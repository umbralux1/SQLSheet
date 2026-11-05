// Lets scripts/build_results.py talk to PGlite: one JSON request per line on stdin,
// one JSON reply per line on stdout. Uses the same code as the browser (static/pg-core.js).
import { createInterface } from 'node:readline';
import { PGlite } from '@electric-sql/pglite';
import { runSql, clearDatabase, readTables, errorInfo } from '../static/pg-core.js';

const db = new PGlite();
await db.waitReady;

const ops = {
  version: async () => (await db.query('SELECT version() AS v')).rows[0].v,
  run: ({ sql }) => runSql(db, sql),
  reset: async ({ seed }) => { await clearDatabase(db); await runSql(db, seed); return true; },
  tables: () => readTables(db),
};

for await (const line of createInterface({ input: process.stdin })) {
  const request = JSON.parse(line);
  let reply;
  try {
    reply = { result: await ops[request.op](request) };
  } catch (e) {
    reply = { error: errorInfo(e) };
  }
  process.stdout.write(JSON.stringify(reply) + '\n');
}
process.exit(0);

/* PostgreSQL (PGlite) in its own thread, so a slow query cannot freeze the page.
   Keep this version equal to the one in package.json: the expected answers are worked out with it. */
import { PGlite } from 'https://cdn.jsdelivr.net/npm/@electric-sql/pglite@0.5.11/dist/index.js';
import { runSql, clearDatabase, readTables, errorInfo } from './pg-core.js';

let db = null;

const ops = {
  run: ({ sql }) => runSql(db, sql),
  reset: async ({ seed }) => { await clearDatabase(db); await runSql(db, seed); },
  tables: () => readTables(db),
};

self.onmessage = async ({ data }) => {
  try {
    if (!db) { db = new PGlite(); await db.waitReady; }
    self.postMessage({ id: data.id, result: await ops[data.op](data) });
  } catch (e) {
    self.postMessage({ id: data.id, error: errorInfo(e) });
  }
};

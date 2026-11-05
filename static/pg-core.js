/* How SQL runs on PGlite. Shared by the browser (pg-worker.js) and by the tool that
   works out the expected answers (scripts/pg_bridge.mjs), so a student's result and
   the expected one always come out in exactly the same format. */

const text = v => v;
const number = v => { const n = Number(v); return Number.isFinite(n) ? n : v };
const wholeNumber = v => { const n = Number(v); return Number.isSafeInteger(n) ? n : v };

/* Values arrive as JSON-friendly data: dates and JSON stay text as PostgreSQL prints them,
   numeric and bigint become plain numbers (a value too big for that stays text). */
export const PARSERS = {
  20: wholeNumber,    // bigint
  1700: number,       // numeric
  1082: text,         // date
  1083: text,         // time
  1114: text,         // timestamp
  1184: text,         // timestamptz
  1186: text,         // interval
  1266: text,         // timetz
  114: text,          // json
  3802: text,         // jsonb
};

function plain(v) {
  if (typeof v === 'bigint') return String(v);
  if (Array.isArray(v)) return '{' + v.map(x => x === null ? 'NULL' : plain(x)).join(',') + '}';
  return v;
}

/* Runs one or more statements. One result per statement:
   {columns, rows, returnsRows, affected}. All of them run as one transaction, as in
   PostgreSQL: an error in the last statement undoes the ones before it. */
export async function runSql(db, sql) {
  const results = await db.exec(sql, { rowMode: 'array', parsers: PARSERS });
  let before = 0;
  return results.map(r => {
    const affected = (r.affectedRows || 0) - before;   // PGlite counts up across the statements
    before = r.affectedRows || 0;
    return {
      columns: r.fields.map(f => f.name),
      rows: r.rows.map(row => row.map(plain)),
      returnsRows: r.fields.length > 0,
      affected,
    };
  });
}

/* Back to an empty database, whatever the student did: open transaction, settings, roles, schemas. */
export async function clearDatabase(db) {
  await db.exec('ROLLBACK');
  await db.exec('DISCARD ALL');
  const { rows } = await db.query(
    "SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg\\_%' AND nspname <> 'information_schema'");
  const drops = rows.map(r => `DROP SCHEMA "${r.nspname.replace(/"/g, '""')}" CASCADE;`).join(' ');
  await db.exec(drops + ' CREATE SCHEMA public;');
}

export function errorInfo(e) {
  return { message: e.message, hint: e.hint, code: e.code, position: e.position };
}

/* Every table of the public schema, in the order they were created. Shown as sheets and in the
   sidebar. key lists the primary key's columns: rows are sorted by it, and it tells which row
   changed. Without one, a row is known by its whole content. */
const ROW_LIMIT = 5000;
export async function readTables(db) {
  const { rows } = await db.query(`
    SELECT c.relname AS table_name, a.attname AS name, format_type(a.atttypid, a.atttypmod) AS type,
           a.attnum = ANY(COALESCE(i.indkey::int2[], '{}')) AS pk
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped
    LEFT JOIN pg_index i ON i.indrelid = c.oid AND i.indisprimary
    WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
    ORDER BY c.oid, a.attnum`);
  const tables = [];
  for (const r of rows) {
    if (!tables.length || tables[tables.length - 1].name !== r.table_name) tables.push({ name: r.table_name, columns: [] });
    tables[tables.length - 1].columns.push({ name: r.name, type: r.type.replace('character varying', 'varchar'), pk: r.pk });
  }
  const q = s => '"' + s.replace(/"/g, '""') + '"';
  for (const t of tables) {
    const key = t.columns.filter(c => c.pk).map(c => q(c.name)).join(', ');
    const [count, data] = await runSql(db,
      `SELECT count(*) FROM ${q(t.name)}; SELECT * FROM ${q(t.name)} ORDER BY ${key || 'ctid'} LIMIT ${ROW_LIMIT};`);
    t.count = count.rows[0][0];
    t.rows = data.rows;
  }
  return tables;
}

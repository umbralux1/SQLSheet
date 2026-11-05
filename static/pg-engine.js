/* The page's one way to the database. Every tab has its own database on the server (pg_engine.py):

     run(sql)    -> [{columns, rows, returnsRows, affected}, ...], one per statement
     reset(seed) -> back to a database with only the seed's data; the first call creates it
     tables()    -> [{name, columns: [{name, type, pk}], count, rows}, ...]

   A failed call rejects with PostgreSQL's message, hint, code and position. When the server no
   longer has this tab's database, the error has lost = true, and the caller reseeds. */
class PgEngine {
  constructor() {
    const bytes = crypto.getRandomValues(new Uint8Array(16));   // randomUUID needs https; make run-lan is http
    this.session = Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
    addEventListener('pagehide', () => navigator.sendBeacon(`/api/db/${this.session}/close`));
  }

  async call(body) {
    const response = await fetch(`/api/db/${this.session}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (data.error) throw Object.assign(new Error(data.error.message), data.error);
    return data.result;
  }

  run(sql) { return this.call({ op: 'run', sql }) }
  reset(seed) { return this.call({ op: 'reset', sql: seed }) }
  tables() { return this.call({ op: 'tables' }) }
}

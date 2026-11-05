/* The page's one way to the database. A room has one database on the server (pg_engine.py), and
   this page has its own connection to it, so its open transaction is its own:

     open(key, lang, seed)  -> {lang, reset}: on the page's start. Data stays if the room already
                               holds lesson `key`; otherwise everyone's data becomes the seed
     reset(key, lang, seed) -> {lang, reset}: back to only the seed's data, for everyone in the room
     run(sql)    -> [{columns, rows, returnsRows, affected}, ...], one per statement
     tables()    -> [{name, columns: [{name, type, pk}], count, rows}, ...]

   A failed call rejects with PostgreSQL's message, hint, code and position. When the server no
   longer has the room's database, the error has lost = true, and the caller reseeds. */
class PgEngine {
  constructor(room) {
    this.room = room;
    const bytes = crypto.getRandomValues(new Uint8Array(16));   // randomUUID needs https; make run-lan is http
    this.client = Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
    addEventListener('pagehide', () => navigator.sendBeacon('/api/db/close',
      new Blob([JSON.stringify({ room: this.room, client: this.client })], { type: 'application/json' })));
  }

  async call(body) {
    const response = await fetch('/api/db', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ room: this.room, client: this.client, ...body }),
    });
    const data = await response.json();
    if (data.error) throw Object.assign(new Error(data.error.message), data.error);
    return data.result;
  }

  open(key, lang, seed) { return this.call({ op: 'open', key, lang, sql: seed }) }
  reset(key, lang, seed) { return this.call({ op: 'reset', key, lang, sql: seed }) }
  run(sql) { return this.call({ op: 'run', sql }) }
  tables() { return this.call({ op: 'tables' }) }
}

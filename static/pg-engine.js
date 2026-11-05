/* The page's one way to the database. Lessons call only these methods and never PGlite itself,
   so a lesson that needs a real server (several connections at once) can get another engine
   with the same methods:

     run(sql)    -> [{columns, rows, returnsRows, affected}, ...], one per statement
     reset(seed) -> back to a database with only the seed's data
     tables()    -> [{name, columns: [{name, type, pk}], count, rows}, ...]

   PGlite cannot enforce statement_timeout, so a query that runs too long is stopped by
   throwing the whole thread away. The data goes with it: the error has timedOut = true,
   and the caller reseeds. */
class PgEngine {
  constructor({ timeoutMs = 20000 } = {}) {
    this.timeoutMs = timeoutMs;
    this.nextId = 1;
    this.waiting = new Map();
    this.startWorker();
  }

  startWorker() {
    this.worker = new Worker('static/pg-worker.js', { type: 'module' });
    this.worker.onmessage = ({ data }) => {
      const call = this.waiting.get(data.id);
      if (!call) return;
      this.waiting.delete(data.id);
      clearTimeout(call.timer);
      if (data.error) call.reject(Object.assign(new Error(data.error.message), data.error));
      else call.resolve(data.result);
    };
    this.worker.onerror = e => this.failAll(new Error(e.message || 'the engine did not load'));
  }

  failAll(error) {
    this.waiting.forEach(call => { clearTimeout(call.timer); call.reject(error) });
    this.waiting.clear();
  }

  restart() {
    this.worker.terminate();
    this.failAll(Object.assign(new Error('The query ran too long and was stopped.'), { timedOut: true }));
    this.startWorker();
  }

  call(op, args, limited) {
    return new Promise((resolve, reject) => {
      const id = this.nextId++;
      const timer = limited ? setTimeout(() => this.restart(), this.timeoutMs) : null;
      this.waiting.set(id, { resolve, reject, timer });
      this.worker.postMessage({ id, op, ...args });
    });
  }

  run(sql) { return this.call('run', { sql }, true) }
  reset(seed) { return this.call('reset', { seed }, false) }   // the first call also waits for the engine to start
  tables() { return this.call('tables', {}, true) }
}

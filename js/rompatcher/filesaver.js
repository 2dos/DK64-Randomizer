/* FileSaver.js (source: http://purl.eligrey.com/github/FileSaver.js/blob/master/src/FileSaver.js)
 * A saveAs() FileSaver implementation.
 * 1.3.8
 * 2018-03-22 14:03:47
 *
 * By Eli Grey, https://eligrey.com
 * License: MIT
 *   See https://github.com/eligrey/FileSaver.js/blob/master/LICENSE.md
 */
var saveAs =
  saveAs ||
  (function (c) {
    'use strict'
    if (
      !(
        void 0 === c ||
        (typeof navigator !== 'undefined' &&
          /MSIE [1-9]\./.test(navigator.userAgent))
      )
    ) {
      const t = c.document
      const f = function () {
        return c.URL || c.webkitURL || c
      }
      const s = t.createElementNS('http://www.w3.org/1999/xhtml', 'a')
      const d = 'download' in s
      const u = /constructor/i.test(c.HTMLElement) || c.safari
      const l = /CriOS\/[\d]+/.test(navigator.userAgent)
      const p = c.setImmediate || c.setTimeout
      const v = function (t) {
        p(function () {
          throw t
        }, 0)
      }
      const w = function (t) {
        setTimeout(function () {
          typeof t === 'string' ? f().revokeObjectURL(t) : t.remove()
        }, 4e4)
      }
      const m = function (t) {
        return /^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(
          t.type
        )
          ? new Blob([String.fromCharCode(65279), t], { type: t.type })
          : t
      }
      const r = function (t, n, e) {
        e || (t = m(t))
        let r
        const o = this
        const a = t.type === 'application/octet-stream'
        const i = function () {
          !(function (t, e, n) {
            for (let r = (e = [].concat(e)).length; r--;) {
              const o = t['on' + e[r]]
              if (typeof o === 'function') {
                try {
                  o.call(t, n || t)
                } catch (t) {
                  v(t)
                }
              }
            }
          })(o, 'writestart progress write writeend'.split(' '))
        }
        if (((o.readyState = o.INIT), d)) {
          return (
            (r = f().createObjectURL(t)),
            void p(function () {
              let t, e;
              (s.href = r),
              (s.download = n),
              (t = s),
              (e = new MouseEvent('click')),
              t.dispatchEvent(e),
              i(),
              w(r),
              (o.readyState = o.DONE)
            }, 0)
          )
        }
        !(function () {
          if ((l || (a && u)) && c.FileReader) {
            const e = new FileReader()
            return (
              (e.onloadend = function () {
                let t = l
                  ? e.result
                  : e.result.replace(/^data:[^;]*;/, 'data:attachment/file;')
                c.open(t, '_blank') || (c.location.href = t),
                (t = void 0),
                (o.readyState = o.DONE),
                i()
              }),
              e.readAsDataURL(t),
              (o.readyState = o.INIT)
            )
          }
          r || (r = f().createObjectURL(t)),
          a
            ? (c.location.href = r)
            : c.open(r, '_blank') || (c.location.href = r);
          (o.readyState = o.DONE), i(), w(r)
        })()
      }
      const e = r.prototype
      return typeof navigator !== 'undefined' && navigator.msSaveOrOpenBlob
        ? function (t, e, n) {
            return (
              (e = e || t.name || 'download'),
              n || (t = m(t)),
              navigator.msSaveOrOpenBlob(t, e)
            )
          }
        : ((e.abort = function () {}),
          (e.readyState = e.INIT = 0),
          (e.WRITING = 1),
          (e.DONE = 2),
          (e.error = e.onwritestart = e.onprogress = e.onwrite = e.onabort = e.onerror = e.onwriteend = null),
          function (t, e, n) {
            return new r(t, e || t.name || 'download', n)
          })
    }
  })(
    (typeof self !== 'undefined' && self) ||
      (typeof window !== 'undefined' && window) ||
      this
  )

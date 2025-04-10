import { i as ur, a as Rt, r as fr, w as We, g as dr, d as pr, b as Ae, c as oe, e as mr } from "./Index-8WNfBRlo.js";
const F = window.ms_globals.React, l = window.ms_globals.React, Ye = window.ms_globals.React.useMemo, Dt = window.ms_globals.React.useState, we = window.ms_globals.React.useEffect, sr = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, ar = window.ms_globals.React.version, lr = window.ms_globals.React.isValidElement, cr = window.ms_globals.React.useLayoutEffect, Vt = window.ms_globals.ReactDOM, qe = window.ms_globals.ReactDOM.createPortal, hr = window.ms_globals.internalContext.useContextPropsContext, gr = window.ms_globals.internalContext.ContextPropsProvider, vr = window.ms_globals.antd.ConfigProvider, Ln = window.ms_globals.antd.Upload, ke = window.ms_globals.antd.theme, br = window.ms_globals.antd.Progress, yr = window.ms_globals.antd.Image, pt = window.ms_globals.antd.Button, Sr = window.ms_globals.antd.Flex, mt = window.ms_globals.antd.Typography, wr = window.ms_globals.antdIcons.FileTextFilled, xr = window.ms_globals.antdIcons.CloseCircleFilled, Er = window.ms_globals.antdIcons.FileExcelFilled, Cr = window.ms_globals.antdIcons.FileImageFilled, _r = window.ms_globals.antdIcons.FileMarkdownFilled, Rr = window.ms_globals.antdIcons.FilePdfFilled, Lr = window.ms_globals.antdIcons.FilePptFilled, Ir = window.ms_globals.antdIcons.FileWordFilled, Tr = window.ms_globals.antdIcons.FileZipFilled, Pr = window.ms_globals.antdIcons.PlusOutlined, Mr = window.ms_globals.antdIcons.LeftOutlined, Or = window.ms_globals.antdIcons.RightOutlined, Xt = window.ms_globals.antdCssinjs.unit, ht = window.ms_globals.antdCssinjs.token2CSSVar, Wt = window.ms_globals.antdCssinjs.useStyleRegister, Fr = window.ms_globals.antdCssinjs.useCSSVarRegister, Ar = window.ms_globals.antdCssinjs.createTheme, $r = window.ms_globals.antdCssinjs.useCacheToken;
var kr = /\s/;
function jr(e) {
  for (var t = e.length; t-- && kr.test(e.charAt(t)); )
    ;
  return t;
}
var Dr = /^\s+/;
function Nr(e) {
  return e && e.slice(0, jr(e) + 1).replace(Dr, "");
}
var Gt = NaN, zr = /^[-+]0x[0-9a-f]+$/i, Hr = /^0b[01]+$/i, Ur = /^0o[0-7]+$/i, Br = parseInt;
function Kt(e) {
  if (typeof e == "number")
    return e;
  if (ur(e))
    return Gt;
  if (Rt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Rt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Nr(e);
  var n = Hr.test(e);
  return n || Ur.test(e) ? Br(e.slice(2), n ? 2 : 8) : zr.test(e) ? Gt : +e;
}
function Vr() {
}
var gt = function() {
  return fr.Date.now();
}, Xr = "Expected a function", Wr = Math.max, Gr = Math.min;
function Kr(e, t, n) {
  var r, o, i, s, a, c, u = 0, p = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Xr);
  t = Kt(t) || 0, Rt(n) && (p = !!n.leading, f = "maxWait" in n, i = f ? Wr(Kt(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function m(v) {
    var R = r, S = o;
    return r = o = void 0, u = v, s = e.apply(S, R), s;
  }
  function y(v) {
    return u = v, a = setTimeout(b, t), p ? m(v) : s;
  }
  function w(v) {
    var R = v - c, S = v - u, T = t - R;
    return f ? Gr(T, i - S) : T;
  }
  function h(v) {
    var R = v - c, S = v - u;
    return c === void 0 || R >= t || R < 0 || f && S >= i;
  }
  function b() {
    var v = gt();
    if (h(v))
      return E(v);
    a = setTimeout(b, w(v));
  }
  function E(v) {
    return a = void 0, d && r ? m(v) : (r = o = void 0, s);
  }
  function C() {
    a !== void 0 && clearTimeout(a), u = 0, r = c = o = a = void 0;
  }
  function g() {
    return a === void 0 ? s : E(gt());
  }
  function x() {
    var v = gt(), R = h(v);
    if (r = arguments, o = this, c = v, R) {
      if (a === void 0)
        return y(c);
      if (f)
        return clearTimeout(a), a = setTimeout(b, t), m(c);
    }
    return a === void 0 && (a = setTimeout(b, t)), s;
  }
  return x.cancel = C, x.flush = g, x;
}
var In = {
  exports: {}
}, Je = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var qr = l, Zr = Symbol.for("react.element"), Qr = Symbol.for("react.fragment"), Yr = Object.prototype.hasOwnProperty, Jr = qr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, eo = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Tn(e, t, n) {
  var r, o = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) Yr.call(t, r) && !eo.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Zr,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: Jr.current
  };
}
Je.Fragment = Qr;
Je.jsx = Tn;
Je.jsxs = Tn;
In.exports = Je;
var te = In.exports;
const {
  SvelteComponent: to,
  assign: qt,
  binding_callbacks: Zt,
  check_outros: no,
  children: Pn,
  claim_element: Mn,
  claim_space: ro,
  component_subscribe: Qt,
  compute_slots: oo,
  create_slot: io,
  detach: _e,
  element: On,
  empty: Yt,
  exclude_internal_props: Jt,
  get_all_dirty_from_scope: so,
  get_slot_changes: ao,
  group_outros: lo,
  init: co,
  insert_hydration: Ge,
  safe_not_equal: uo,
  set_custom_element_data: Fn,
  space: fo,
  transition_in: Ke,
  transition_out: Lt,
  update_slot_base: po
} = window.__gradio__svelte__internal, {
  beforeUpdate: mo,
  getContext: ho,
  onDestroy: go,
  setContext: vo
} = window.__gradio__svelte__internal;
function en(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = io(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = On("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Mn(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Pn(t);
      o && o.l(s), s.forEach(_e), this.h();
    },
    h() {
      Fn(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ge(i, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && po(
        o,
        r,
        i,
        /*$$scope*/
        i[6],
        n ? ao(
          r,
          /*$$scope*/
          i[6],
          s,
          null
        ) : so(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (Ke(o, i), n = !0);
    },
    o(i) {
      Lt(o, i), n = !1;
    },
    d(i) {
      i && _e(t), o && o.d(i), e[9](null);
    }
  };
}
function bo(e) {
  let t, n, r, o, i = (
    /*$$slots*/
    e[4].default && en(e)
  );
  return {
    c() {
      t = On("react-portal-target"), n = fo(), i && i.c(), r = Yt(), this.h();
    },
    l(s) {
      t = Mn(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Pn(t).forEach(_e), n = ro(s), i && i.l(s), r = Yt(), this.h();
    },
    h() {
      Fn(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ge(s, t, a), e[8](t), Ge(s, n, a), i && i.m(s, a), Ge(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Ke(i, 1)) : (i = en(s), i.c(), Ke(i, 1), i.m(r.parentNode, r)) : i && (lo(), Lt(i, 1, 1, () => {
        i = null;
      }), no());
    },
    i(s) {
      o || (Ke(i), o = !0);
    },
    o(s) {
      Lt(i), o = !1;
    },
    d(s) {
      s && (_e(t), _e(n), _e(r)), e[8](null), i && i.d(s);
    }
  };
}
function tn(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function yo(e, t, n) {
  let r, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = oo(i);
  let {
    svelteInit: c
  } = t;
  const u = We(tn(t)), p = We();
  Qt(e, p, (g) => n(0, r = g));
  const f = We();
  Qt(e, f, (g) => n(1, o = g));
  const d = [], m = ho("$$ms-gr-react-wrapper"), {
    slotKey: y,
    slotIndex: w,
    subSlotIndex: h
  } = dr() || {}, b = c({
    parent: m,
    props: u,
    target: p,
    slot: f,
    slotKey: y,
    slotIndex: w,
    subSlotIndex: h,
    onDestroy(g) {
      d.push(g);
    }
  });
  vo("$$ms-gr-react-wrapper", b), mo(() => {
    u.set(tn(t));
  }), go(() => {
    d.forEach((g) => g());
  });
  function E(g) {
    Zt[g ? "unshift" : "push"](() => {
      r = g, p.set(r);
    });
  }
  function C(g) {
    Zt[g ? "unshift" : "push"](() => {
      o = g, f.set(o);
    });
  }
  return e.$$set = (g) => {
    n(17, t = qt(qt({}, t), Jt(g))), "svelteInit" in g && n(5, c = g.svelteInit), "$$scope" in g && n(6, s = g.$$scope);
  }, t = Jt(t), [r, o, p, f, a, c, s, i, E, C];
}
class So extends to {
  constructor(t) {
    super(), co(this, t, yo, bo, uo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: ms
} = window.__gradio__svelte__internal, nn = window.ms_globals.rerender, vt = window.ms_globals.tree;
function wo(e, t = {}) {
  function n(r) {
    const o = We(), i = new So({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? vt;
          return c.nodes = [...c.nodes, a], nn({
            createPortal: qe,
            node: vt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), nn({
              createPortal: qe,
              node: vt
            });
          }), a;
        },
        ...r.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
function xo(e) {
  const [t, n] = Dt(() => Ae(e));
  return we(() => {
    let r = !0;
    return e.subscribe((i) => {
      r && (r = !1, i === t) || n(i);
    });
  }, [e]), t;
}
function Eo(e) {
  const t = Ye(() => pr(e, (n) => n), [e]);
  return xo(t);
}
const Co = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function _o(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = Ro(n, r), t;
  }, {}) : {};
}
function Ro(e, t) {
  return typeof t == "number" && !Co.includes(e) ? t + "px" : t;
}
function It(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = l.Children.toArray(e._reactElement.props.children).map((i) => {
      if (l.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = It(i.props.el);
        return l.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...l.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(qe(l.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, s, c);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const i = r[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = It(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Lo(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const $e = sr(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, i) => {
  const s = he(), [a, c] = Dt([]), {
    forceClone: u
  } = hr(), p = u ? !0 : t;
  return we(() => {
    var w;
    if (!s.current || !e)
      return;
    let f = e;
    function d() {
      let h = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (h = f.children[0], h.tagName.toLowerCase() === "react-portal-target" && h.children[0] && (h = h.children[0])), Lo(i, h), n && h.classList.add(...n.split(" ")), r) {
        const b = _o(r);
        Object.keys(b).forEach((E) => {
          h.style[E] = b[E];
        });
      }
    }
    let m = null, y = null;
    if (p && window.MutationObserver) {
      let h = function() {
        var g, x, v;
        (g = s.current) != null && g.contains(f) && ((x = s.current) == null || x.removeChild(f));
        const {
          portals: E,
          clonedElement: C
        } = It(e);
        f = C, c(E), f.style.display = "contents", y && clearTimeout(y), y = setTimeout(() => {
          d();
        }, 50), (v = s.current) == null || v.appendChild(f);
      };
      h();
      const b = Kr(() => {
        h(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      m = new window.MutationObserver(b), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (w = s.current) == null || w.appendChild(f);
    return () => {
      var h, b;
      f.style.display = "", (h = s.current) != null && h.contains(f) && ((b = s.current) == null || b.removeChild(f)), m == null || m.disconnect();
    };
  }, [e, p, n, r, i, o, u]), l.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Io = "1.1.0", To = /* @__PURE__ */ l.createContext({}), Po = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Mo = (e) => {
  const t = l.useContext(To);
  return l.useMemo(() => ({
    ...Po,
    ...t[e]
  }), [t[e]]);
};
function Ie() {
  return Ie = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, Ie.apply(null, arguments);
}
function Ze() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r,
    theme: o
  } = l.useContext(vr.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r
  };
}
function Te(e) {
  var t = F.useRef();
  t.current = e;
  var n = F.useCallback(function() {
    for (var r, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return n;
}
function Oo(e) {
  if (Array.isArray(e)) return e;
}
function Fo(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (r = i.call(n)).done) && (a.push(r.value), a.length !== t); c = !0) ;
    } catch (p) {
      u = !0, o = p;
    } finally {
      try {
        if (!c && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function rn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function Ao(e, t) {
  if (e) {
    if (typeof e == "string") return rn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? rn(e, t) : void 0;
  }
}
function $o() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ee(e, t) {
  return Oo(e) || Fo(e, t) || Ao(e, t) || $o();
}
function et() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var on = et() ? F.useLayoutEffect : F.useEffect, ko = function(t, n) {
  var r = F.useRef(!0);
  on(function() {
    return t(r.current);
  }, n), on(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, sn = function(t, n) {
  ko(function(r) {
    if (!r)
      return t();
  }, n);
};
function je(e) {
  var t = F.useRef(!1), n = F.useState(e), r = ee(n, 2), o = r[0], i = r[1];
  F.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [o, s];
}
function bt(e) {
  return e !== void 0;
}
function jo(e, t) {
  var n = t || {}, r = n.defaultValue, o = n.value, i = n.onChange, s = n.postState, a = je(function() {
    return bt(o) ? o : bt(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), c = ee(a, 2), u = c[0], p = c[1], f = o !== void 0 ? o : u, d = s ? s(f) : f, m = Te(i), y = je([f]), w = ee(y, 2), h = w[0], b = w[1];
  sn(function() {
    var C = h[0];
    u !== C && m(u, C);
  }, [h]), sn(function() {
    bt(o) || p(o);
  }, [o]);
  var E = Te(function(C, g) {
    p(C, g), b([f], g);
  });
  return [d, E];
}
function q(e) {
  "@babel/helpers - typeof";
  return q = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, q(e);
}
var An = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Nt = Symbol.for("react.element"), zt = Symbol.for("react.portal"), tt = Symbol.for("react.fragment"), nt = Symbol.for("react.strict_mode"), rt = Symbol.for("react.profiler"), ot = Symbol.for("react.provider"), it = Symbol.for("react.context"), Do = Symbol.for("react.server_context"), st = Symbol.for("react.forward_ref"), at = Symbol.for("react.suspense"), lt = Symbol.for("react.suspense_list"), ct = Symbol.for("react.memo"), ut = Symbol.for("react.lazy"), No = Symbol.for("react.offscreen"), $n;
$n = Symbol.for("react.module.reference");
function ie(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Nt:
        switch (e = e.type, e) {
          case tt:
          case rt:
          case nt:
          case at:
          case lt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Do:
              case it:
              case st:
              case ut:
              case ct:
              case ot:
                return e;
              default:
                return t;
            }
        }
      case zt:
        return t;
    }
  }
}
A.ContextConsumer = it;
A.ContextProvider = ot;
A.Element = Nt;
A.ForwardRef = st;
A.Fragment = tt;
A.Lazy = ut;
A.Memo = ct;
A.Portal = zt;
A.Profiler = rt;
A.StrictMode = nt;
A.Suspense = at;
A.SuspenseList = lt;
A.isAsyncMode = function() {
  return !1;
};
A.isConcurrentMode = function() {
  return !1;
};
A.isContextConsumer = function(e) {
  return ie(e) === it;
};
A.isContextProvider = function(e) {
  return ie(e) === ot;
};
A.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Nt;
};
A.isForwardRef = function(e) {
  return ie(e) === st;
};
A.isFragment = function(e) {
  return ie(e) === tt;
};
A.isLazy = function(e) {
  return ie(e) === ut;
};
A.isMemo = function(e) {
  return ie(e) === ct;
};
A.isPortal = function(e) {
  return ie(e) === zt;
};
A.isProfiler = function(e) {
  return ie(e) === rt;
};
A.isStrictMode = function(e) {
  return ie(e) === nt;
};
A.isSuspense = function(e) {
  return ie(e) === at;
};
A.isSuspenseList = function(e) {
  return ie(e) === lt;
};
A.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === tt || e === rt || e === nt || e === at || e === lt || e === No || typeof e == "object" && e !== null && (e.$$typeof === ut || e.$$typeof === ct || e.$$typeof === ot || e.$$typeof === it || e.$$typeof === st || e.$$typeof === $n || e.getModuleId !== void 0);
};
A.typeOf = ie;
An.exports = A;
var yt = An.exports, zo = Symbol.for("react.element"), Ho = Symbol.for("react.transitional.element"), Uo = Symbol.for("react.fragment");
function Bo(e) {
  return (
    // Base object type
    e && q(e) === "object" && // React Element type
    (e.$$typeof === zo || e.$$typeof === Ho) && // React Fragment type
    e.type === Uo
  );
}
var Vo = Number(ar.split(".")[0]), Xo = function(t, n) {
  typeof t == "function" ? t(n) : q(t) === "object" && t && "current" in t && (t.current = n);
}, Wo = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (kn(t) && Vo >= 19)
    return !0;
  var o = yt.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== yt.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== yt.ForwardRef);
};
function kn(e) {
  return /* @__PURE__ */ lr(e) && !Bo(e);
}
var Go = function(t) {
  if (t && kn(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function Ko(e, t) {
  if (q(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t);
    if (q(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function jn(e) {
  var t = Ko(e, "string");
  return q(t) == "symbol" ? t : t + "";
}
function I(e, t, n) {
  return (t = jn(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function an(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function L(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? an(Object(n), !0).forEach(function(r) {
      I(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : an(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
const De = /* @__PURE__ */ l.createContext(null);
function ln(e) {
  const {
    getDropContainer: t,
    className: n,
    prefixCls: r,
    children: o
  } = e, {
    disabled: i
  } = l.useContext(De), [s, a] = l.useState(), [c, u] = l.useState(null);
  if (l.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), l.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, m = (h) => {
        h.preventDefault();
      }, y = (h) => {
        h.relatedTarget || u(!1);
      }, w = (h) => {
        u(!1), h.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", m), document.addEventListener("dragleave", y), document.addEventListener("drop", w), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", y), document.removeEventListener("drop", w);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${r}-drop-area`;
  return /* @__PURE__ */ qe(/* @__PURE__ */ l.createElement("div", {
    className: oe(f, n, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, o), s);
}
function cn(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function qo(e) {
  return e && q(e) === "object" && cn(e.nativeElement) ? e.nativeElement : cn(e) ? e : null;
}
function Zo(e) {
  var t = qo(e);
  if (t)
    return t;
  if (e instanceof l.Component) {
    var n;
    return (n = Vt.findDOMNode) === null || n === void 0 ? void 0 : n.call(Vt, e);
  }
  return null;
}
function Qo(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.indexOf(r) !== -1) continue;
    n[r] = e[r];
  }
  return n;
}
function un(e, t) {
  if (e == null) return {};
  var n, r, o = Qo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) n = i[r], t.indexOf(n) === -1 && {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var Yo = /* @__PURE__ */ F.createContext({});
function Pe(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function fn(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, jn(r.key), r);
  }
}
function Me(e, t, n) {
  return t && fn(e.prototype, t), n && fn(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Tt(e, t) {
  return Tt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Tt(e, t);
}
function ft(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Tt(e, t);
}
function Qe(e) {
  return Qe = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Qe(e);
}
function Dn() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Dn = function() {
    return !!e;
  })();
}
function xe(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Jo(e, t) {
  if (t && (q(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return xe(e);
}
function dt(e) {
  var t = Dn();
  return function() {
    var n, r = Qe(e);
    if (t) {
      var o = Qe(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return Jo(this, n);
  };
}
var ei = /* @__PURE__ */ function(e) {
  ft(n, e);
  var t = dt(n);
  function n() {
    return Pe(this, n), t.apply(this, arguments);
  }
  return Me(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(F.Component);
function ti(e) {
  var t = F.useReducer(function(a) {
    return a + 1;
  }, 0), n = ee(t, 2), r = n[1], o = F.useRef(e), i = Te(function() {
    return o.current;
  }), s = Te(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, r();
  });
  return [i, s];
}
var ve = "none", ze = "appear", He = "enter", Ue = "leave", dn = "none", ae = "prepare", Re = "start", Le = "active", Ht = "end", Nn = "prepared";
function pn(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function ni(e, t) {
  var n = {
    animationend: pn("Animation", "AnimationEnd"),
    transitionend: pn("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var ri = ni(et(), typeof window < "u" ? window : {}), zn = {};
if (et()) {
  var oi = document.createElement("div");
  zn = oi.style;
}
var Be = {};
function Hn(e) {
  if (Be[e])
    return Be[e];
  var t = ri[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var i = n[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in zn)
        return Be[e] = t[i], Be[e];
    }
  return "";
}
var Un = Hn("animationend"), Bn = Hn("transitionend"), Vn = !!(Un && Bn), mn = Un || "animationend", hn = Bn || "transitionend";
function gn(e, t) {
  if (!e) return null;
  if (q(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const ii = function(e) {
  var t = he();
  function n(o) {
    o && (o.removeEventListener(hn, e), o.removeEventListener(mn, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(hn, e), o.addEventListener(mn, e), t.current = o);
  }
  return F.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var Xn = et() ? cr : we, Wn = function(t) {
  return +setTimeout(t, 16);
}, Gn = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Wn = function(t) {
  return window.requestAnimationFrame(t);
}, Gn = function(t) {
  return window.cancelAnimationFrame(t);
});
var vn = 0, Ut = /* @__PURE__ */ new Map();
function Kn(e) {
  Ut.delete(e);
}
var Pt = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  vn += 1;
  var r = vn;
  function o(i) {
    if (i === 0)
      Kn(r), t();
    else {
      var s = Wn(function() {
        o(i - 1);
      });
      Ut.set(r, s);
    }
  }
  return o(n), r;
};
Pt.cancel = function(e) {
  var t = Ut.get(e);
  return Kn(e), Gn(t);
};
const si = function() {
  var e = F.useRef(null);
  function t() {
    Pt.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Pt(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = i;
  }
  return F.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var ai = [ae, Re, Le, Ht], li = [ae, Nn], qn = !1, ci = !0;
function Zn(e) {
  return e === Le || e === Ht;
}
const ui = function(e, t, n) {
  var r = je(dn), o = ee(r, 2), i = o[0], s = o[1], a = si(), c = ee(a, 2), u = c[0], p = c[1];
  function f() {
    s(ae, !0);
  }
  var d = t ? li : ai;
  return Xn(function() {
    if (i !== dn && i !== Ht) {
      var m = d.indexOf(i), y = d[m + 1], w = n(i);
      w === qn ? s(y, !0) : y && u(function(h) {
        function b() {
          h.isCanceled() || s(y, !0);
        }
        w === !0 ? b() : Promise.resolve(w).then(b);
      });
    }
  }, [e, i]), F.useEffect(function() {
    return function() {
      p();
    };
  }, []), [f, i];
};
function fi(e, t, n, r) {
  var o = r.motionEnter, i = o === void 0 ? !0 : o, s = r.motionAppear, a = s === void 0 ? !0 : s, c = r.motionLeave, u = c === void 0 ? !0 : c, p = r.motionDeadline, f = r.motionLeaveImmediately, d = r.onAppearPrepare, m = r.onEnterPrepare, y = r.onLeavePrepare, w = r.onAppearStart, h = r.onEnterStart, b = r.onLeaveStart, E = r.onAppearActive, C = r.onEnterActive, g = r.onLeaveActive, x = r.onAppearEnd, v = r.onEnterEnd, R = r.onLeaveEnd, S = r.onVisibleChanged, T = je(), $ = ee(T, 2), j = $[0], _ = $[1], M = ti(ve), P = ee(M, 2), O = P[0], D = P[1], H = je(null), Z = ee(H, 2), pe = Z[0], le = Z[1], V = O(), N = he(!1), G = he(null);
  function z() {
    return n();
  }
  var Q = he(!1);
  function me() {
    D(ve), le(null, !0);
  }
  var se = Te(function(K) {
    var U = O();
    if (U !== ve) {
      var k = z();
      if (!(K && !K.deadline && K.target !== k)) {
        var Ce = Q.current, Ne;
        U === ze && Ce ? Ne = x == null ? void 0 : x(k, K) : U === He && Ce ? Ne = v == null ? void 0 : v(k, K) : U === Ue && Ce && (Ne = R == null ? void 0 : R(k, K)), Ce && Ne !== !1 && me();
      }
    }
  }), Oe = ii(se), ce = ee(Oe, 1), ue = ce[0], ge = function(U) {
    switch (U) {
      case ze:
        return I(I(I({}, ae, d), Re, w), Le, E);
      case He:
        return I(I(I({}, ae, m), Re, h), Le, C);
      case Ue:
        return I(I(I({}, ae, y), Re, b), Le, g);
      default:
        return {};
    }
  }, fe = F.useMemo(function() {
    return ge(V);
  }, [V]), be = ui(V, !e, function(K) {
    if (K === ae) {
      var U = fe[ae];
      return U ? U(z()) : qn;
    }
    if (B in fe) {
      var k;
      le(((k = fe[B]) === null || k === void 0 ? void 0 : k.call(fe, z(), null)) || null);
    }
    return B === Le && V !== ve && (ue(z()), p > 0 && (clearTimeout(G.current), G.current = setTimeout(function() {
      se({
        deadline: !0
      });
    }, p))), B === Nn && me(), ci;
  }), ne = ee(be, 2), X = ne[0], B = ne[1], ye = Zn(B);
  Q.current = ye;
  var Y = he(null);
  Xn(function() {
    if (!(N.current && Y.current === t)) {
      _(t);
      var K = N.current;
      N.current = !0;
      var U;
      !K && t && a && (U = ze), K && t && i && (U = He), (K && !t && u || !K && f && !t && u) && (U = Ue);
      var k = ge(U);
      U && (e || k[ae]) ? (D(U), X()) : D(ve), Y.current = t;
    }
  }, [t]), we(function() {
    // Cancel appear
    (V === ze && !a || // Cancel enter
    V === He && !i || // Cancel leave
    V === Ue && !u) && D(ve);
  }, [a, i, u]), we(function() {
    return function() {
      N.current = !1, clearTimeout(G.current);
    };
  }, []);
  var Se = F.useRef(!1);
  we(function() {
    j && (Se.current = !0), j !== void 0 && V === ve && ((Se.current || j) && (S == null || S(j)), Se.current = !0);
  }, [j, V]);
  var Ee = pe;
  return fe[ae] && B === Re && (Ee = L({
    transition: "none"
  }, Ee)), [V, B, Ee, j ?? t];
}
function di(e) {
  var t = e;
  q(e) === "object" && (t = e.transitionSupport);
  function n(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ F.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, c = o.removeOnLeave, u = c === void 0 ? !0 : c, p = o.forceRender, f = o.children, d = o.motionName, m = o.leavedClassName, y = o.eventProps, w = F.useContext(Yo), h = w.motion, b = n(o, h), E = he(), C = he();
    function g() {
      try {
        return E.current instanceof HTMLElement ? E.current : Zo(C.current);
      } catch {
        return null;
      }
    }
    var x = fi(b, a, g, o), v = ee(x, 4), R = v[0], S = v[1], T = v[2], $ = v[3], j = F.useRef($);
    $ && (j.current = !0);
    var _ = F.useCallback(function(Z) {
      E.current = Z, Xo(i, Z);
    }, [i]), M, P = L(L({}, y), {}, {
      visible: a
    });
    if (!f)
      M = null;
    else if (R === ve)
      $ ? M = f(L({}, P), _) : !u && j.current && m ? M = f(L(L({}, P), {}, {
        className: m
      }), _) : p || !u && !m ? M = f(L(L({}, P), {}, {
        style: {
          display: "none"
        }
      }), _) : M = null;
    else {
      var O;
      S === ae ? O = "prepare" : Zn(S) ? O = "active" : S === Re && (O = "start");
      var D = gn(d, "".concat(R, "-").concat(O));
      M = f(L(L({}, P), {}, {
        className: oe(gn(d, R), I(I({}, D, D && O), d, typeof d == "string")),
        style: T
      }), _);
    }
    if (/* @__PURE__ */ F.isValidElement(M) && Wo(M)) {
      var H = Go(M);
      H || (M = /* @__PURE__ */ F.cloneElement(M, {
        ref: _
      }));
    }
    return /* @__PURE__ */ F.createElement(ei, {
      ref: C
    }, M);
  });
  return r.displayName = "CSSMotion", r;
}
const pi = di(Vn);
var Mt = "add", Ot = "keep", Ft = "remove", St = "removed";
function mi(e) {
  var t;
  return e && q(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, L(L({}, t), {}, {
    key: String(t.key)
  });
}
function At() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(mi);
}
function hi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, i = At(e), s = At(t);
  i.forEach(function(u) {
    for (var p = !1, f = r; f < o; f += 1) {
      var d = s[f];
      if (d.key === u.key) {
        r < f && (n = n.concat(s.slice(r, f).map(function(m) {
          return L(L({}, m), {}, {
            status: Mt
          });
        })), r = f), n.push(L(L({}, d), {}, {
          status: Ot
        })), r += 1, p = !0;
        break;
      }
    }
    p || n.push(L(L({}, u), {}, {
      status: Ft
    }));
  }), r < o && (n = n.concat(s.slice(r).map(function(u) {
    return L(L({}, u), {}, {
      status: Mt
    });
  })));
  var a = {};
  n.forEach(function(u) {
    var p = u.key;
    a[p] = (a[p] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return c.forEach(function(u) {
    n = n.filter(function(p) {
      var f = p.key, d = p.status;
      return f !== u || d !== Ft;
    }), n.forEach(function(p) {
      p.key === u && (p.status = Ot);
    });
  }), n;
}
var gi = ["component", "children", "onVisibleChanged", "onAllRemoved"], vi = ["status"], bi = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function yi(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : pi, n = /* @__PURE__ */ function(r) {
    ft(i, r);
    var o = dt(i);
    function i() {
      var s;
      Pe(this, i);
      for (var a = arguments.length, c = new Array(a), u = 0; u < a; u++)
        c[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(c)), I(xe(s), "state", {
        keyEntities: []
      }), I(xe(s), "removeKey", function(p) {
        s.setState(function(f) {
          var d = f.keyEntities.map(function(m) {
            return m.key !== p ? m : L(L({}, m), {}, {
              status: St
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var f = s.state.keyEntities, d = f.filter(function(m) {
            var y = m.status;
            return y !== St;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Me(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, u = this.props, p = u.component, f = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var m = un(u, gi), y = p || F.Fragment, w = {};
        return bi.forEach(function(h) {
          w[h] = m[h], delete m[h];
        }), delete m.keys, /* @__PURE__ */ F.createElement(y, m, c.map(function(h, b) {
          var E = h.status, C = un(h, vi), g = E === Mt || E === Ot;
          return /* @__PURE__ */ F.createElement(t, Ie({}, w, {
            key: C.key,
            visible: g,
            eventProps: C,
            onVisibleChanged: function(v) {
              d == null || d(v, {
                key: C.key
              }), v || a.removeKey(C.key);
            }
          }), function(x, v) {
            return f(L(L({}, x), {}, {
              index: b
            }), v);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var u = a.keys, p = c.keyEntities, f = At(u), d = hi(p, f);
        return {
          keyEntities: d.filter(function(m) {
            var y = p.find(function(w) {
              var h = w.key;
              return m.key === h;
            });
            return !(y && y.status === St && m.status === Ft);
          })
        };
      }
    }]), i;
  }(F.Component);
  return I(n, "defaultProps", {
    component: "div"
  }), n;
}
const Si = yi(Vn);
function wi(e, t) {
  const {
    children: n,
    upload: r,
    rootClassName: o
  } = e, i = l.useRef(null);
  return l.useImperativeHandle(t, () => i.current), /* @__PURE__ */ l.createElement(Ln, Ie({}, r, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), n);
}
const Qn = /* @__PURE__ */ l.forwardRef(wi);
var Yn = /* @__PURE__ */ Me(function e() {
  Pe(this, e);
}), Jn = "CALC_UNIT", xi = new RegExp(Jn, "g");
function wt(e) {
  return typeof e == "number" ? "".concat(e).concat(Jn) : e;
}
var Ei = /* @__PURE__ */ function(e) {
  ft(n, e);
  var t = dt(n);
  function n(r, o) {
    var i;
    Pe(this, n), i = t.call(this), I(xe(i), "result", ""), I(xe(i), "unitlessCssVar", void 0), I(xe(i), "lowPriority", void 0);
    var s = q(r);
    return i.unitlessCssVar = o, r instanceof n ? i.result = "(".concat(r.result, ")") : s === "number" ? i.result = wt(r) : s === "string" && (i.result = r), i;
  }
  return Me(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(wt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(wt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (c = !1), this.result = this.result.replace(xi, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Yn), Ci = /* @__PURE__ */ function(e) {
  ft(n, e);
  var t = dt(n);
  function n(r) {
    var o;
    return Pe(this, n), o = t.call(this), I(xe(o), "result", 0), r instanceof n ? o.result = r.result : typeof r == "number" && (o.result = r), o;
  }
  return Me(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof n ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof n ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Yn), _i = function(t, n) {
  var r = t === "css" ? Ei : Ci;
  return function(o) {
    return new r(o, n);
  };
}, bn = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function yn(e, t, n, r) {
  var o = L({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var i = r.deprecatedTokens;
    i.forEach(function(a) {
      var c = ee(a, 2), u = c[0], p = c[1];
      if (o != null && o[u] || o != null && o[p]) {
        var f;
        (f = o[p]) !== null && f !== void 0 || (o[p] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = L(L({}, n), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var er = typeof CSSINJS_STATISTIC < "u", $t = !0;
function Bt() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!er)
    return Object.assign.apply(Object, [{}].concat(t));
  $t = !1;
  var r = {};
  return t.forEach(function(o) {
    if (q(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), $t = !0, r;
}
var Sn = {};
function Ri() {
}
var Li = function(t) {
  var n, r = t, o = Ri;
  return er && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(s, a) {
      if ($t) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var c;
    Sn[s] = {
      global: Array.from(n),
      component: L(L({}, (c = Sn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: r,
    keys: n,
    flush: o
  };
};
function wn(e, t, n) {
  if (typeof n == "function") {
    var r;
    return n(Bt(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return n ?? {};
}
function Ii(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "max(".concat(r.map(function(i) {
        return Xt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "min(".concat(r.map(function(i) {
        return Xt(i);
      }).join(","), ")");
    }
  };
}
var Ti = 1e3 * 60 * 10, Pi = /* @__PURE__ */ function() {
  function e() {
    Pe(this, e), I(this, "map", /* @__PURE__ */ new Map()), I(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), I(this, "nextID", 0), I(this, "lastAccessBeat", /* @__PURE__ */ new Map()), I(this, "accessBeat", 0);
  }
  return Me(e, [{
    key: "set",
    value: function(n, r) {
      this.clear();
      var o = this.getCompositeKey(n);
      this.map.set(o, r), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var r = this.getCompositeKey(n), o = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var r = this, o = n.map(function(i) {
        return i && q(i) === "object" ? "obj_".concat(r.getObjectID(i)) : "".concat(q(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var r = this.nextID;
      return this.objectIDMap.set(n, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          r - o > Ti && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), xn = new Pi();
function Mi(e, t) {
  return l.useMemo(function() {
    var n = xn.get(t);
    if (n)
      return n;
    var r = e();
    return xn.set(t, r), r;
  }, t);
}
var Oi = function() {
  return {};
};
function Fi(e) {
  var t = e.useCSP, n = t === void 0 ? Oi : t, r = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, m, y, w) {
    var h = Array.isArray(d) ? d[0] : d;
    function b(S) {
      return "".concat(String(h)).concat(S.slice(0, 1).toUpperCase()).concat(S.slice(1));
    }
    var E = (w == null ? void 0 : w.unitless) || {}, C = typeof a == "function" ? a(d) : {}, g = L(L({}, C), {}, I({}, b("zIndexPopup"), !0));
    Object.keys(E).forEach(function(S) {
      g[b(S)] = E[S];
    });
    var x = L(L({}, w), {}, {
      unitless: g,
      prefixToken: b
    }), v = p(d, m, y, x), R = u(h, y, x);
    return function(S) {
      var T = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : S, $ = v(S, T), j = ee($, 2), _ = j[1], M = R(T), P = ee(M, 2), O = P[0], D = P[1];
      return [O, _, D];
    };
  }
  function u(d, m, y) {
    var w = y.unitless, h = y.injectStyle, b = h === void 0 ? !0 : h, E = y.prefixToken, C = y.ignore, g = function(R) {
      var S = R.rootCls, T = R.cssVar, $ = T === void 0 ? {} : T, j = r(), _ = j.realToken;
      return Fr({
        path: [d],
        prefix: $.prefix,
        key: $.key,
        unitless: w,
        ignore: C,
        token: _,
        scope: S
      }, function() {
        var M = wn(d, _, m), P = yn(d, _, M, {
          deprecatedTokens: y == null ? void 0 : y.deprecatedTokens
        });
        return Object.keys(M).forEach(function(O) {
          P[E(O)] = P[O], delete P[O];
        }), P;
      }), null;
    }, x = function(R) {
      var S = r(), T = S.cssVar;
      return [function($) {
        return b && T ? /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(g, {
          rootCls: R,
          cssVar: T,
          component: d
        }), $) : $;
      }, T == null ? void 0 : T.key];
    };
    return x;
  }
  function p(d, m, y) {
    var w = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = Array.isArray(d) ? d : [d, d], b = ee(h, 1), E = b[0], C = h.join("-"), g = e.layer || {
      name: "antd"
    };
    return function(x) {
      var v = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : x, R = r(), S = R.theme, T = R.realToken, $ = R.hashId, j = R.token, _ = R.cssVar, M = o(), P = M.rootPrefixCls, O = M.iconPrefixCls, D = n(), H = _ ? "css" : "js", Z = Mi(function() {
        var z = /* @__PURE__ */ new Set();
        return _ && Object.keys(w.unitless || {}).forEach(function(Q) {
          z.add(ht(Q, _.prefix)), z.add(ht(Q, bn(E, _.prefix)));
        }), _i(H, z);
      }, [H, E, _ == null ? void 0 : _.prefix]), pe = Ii(H), le = pe.max, V = pe.min, N = {
        theme: S,
        token: j,
        hashId: $,
        nonce: function() {
          return D.nonce;
        },
        clientOnly: w.clientOnly,
        layer: g,
        // antd is always at top of styles
        order: w.order || -999
      };
      typeof i == "function" && Wt(L(L({}, N), {}, {
        clientOnly: !1,
        path: ["Shared", P]
      }), function() {
        return i(j, {
          prefix: {
            rootPrefixCls: P,
            iconPrefixCls: O
          },
          csp: D
        });
      });
      var G = Wt(L(L({}, N), {}, {
        path: [C, x, O]
      }), function() {
        if (w.injectStyle === !1)
          return [];
        var z = Li(j), Q = z.token, me = z.flush, se = wn(E, T, y), Oe = ".".concat(x), ce = yn(E, T, se, {
          deprecatedTokens: w.deprecatedTokens
        });
        _ && se && q(se) === "object" && Object.keys(se).forEach(function(be) {
          se[be] = "var(".concat(ht(be, bn(E, _.prefix)), ")");
        });
        var ue = Bt(Q, {
          componentCls: Oe,
          prefixCls: x,
          iconCls: ".".concat(O),
          antCls: ".".concat(P),
          calc: Z,
          // @ts-ignore
          max: le,
          // @ts-ignore
          min: V
        }, _ ? se : ce), ge = m(ue, {
          hashId: $,
          prefixCls: x,
          rootPrefixCls: P,
          iconPrefixCls: O
        });
        me(E, ce);
        var fe = typeof s == "function" ? s(ue, x, v, w.resetFont) : null;
        return [w.resetStyle === !1 ? null : fe, ge];
      });
      return [G, $];
    };
  }
  function f(d, m, y) {
    var w = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = p(d, m, y, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, w)), b = function(C) {
      var g = C.prefixCls, x = C.rootCls, v = x === void 0 ? g : x;
      return h(g, v), null;
    };
    return b;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: p
  };
}
const W = Math.round;
function xt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = n.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    r[o] = t(r[o] || 0, n[o] || "", o);
  return n[3] ? r[3] = n[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const En = (e, t, n) => n === 0 ? e : e / 100;
function Fe(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class de {
  constructor(t) {
    I(this, "isValid", !0), I(this, "r", 0), I(this, "g", 0), I(this, "b", 0), I(this, "a", 1), I(this, "_h", void 0), I(this, "_s", void 0), I(this, "_l", void 0), I(this, "_v", void 0), I(this, "_max", void 0), I(this, "_min", void 0), I(this, "_brightness", void 0);
    function n(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return r.startsWith(i);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : o("rgb") ? this.fromRgbString(r) : o("hsl") ? this.fromHslString(r) : (o("hsv") || o("hsb")) && this.fromHsvString(r);
    } else if (t instanceof de)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Fe(t.r), this.g = Fe(t.g), this.b = Fe(t.b), this.a = typeof t.a == "number" ? Fe(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), r = t(this.g), o = t(this.b);
    return 0.2126 * n + 0.7152 * r + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = W(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const r = this._c(t), o = n / 100, i = (a) => (r[a] - this[a]) * o + this[a], s = {
      r: W(i("r")),
      g: W(i("g")),
      b: W(i("b")),
      a: W(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), r = this.a + n.a * (1 - this.a), o = (i) => W((this[i] * this.a + n[i] * n.a * (1 - this.a)) / r);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
      a: r
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = W(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
    }
    return t;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const t = this.getHue(), n = W(this.getSaturation() * 100), r = W(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${r}%,${this.a})` : `hsl(${t},${n}%,${r}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(t, n, r) {
    const o = this.clone();
    return o[t] = Fe(n, r), o;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function r(o, i) {
      return parseInt(n[o] + n[i || o], 16);
    }
    n.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = n[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = n[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: r,
    a: o
  }) {
    if (this._h = t % 360, this._s = n, this._l = r, this.a = typeof o == "number" ? o : 1, n <= 0) {
      const d = W(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, u = (1 - Math.abs(2 * r - 1)) * n, p = u * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = u, s = p) : c >= 1 && c < 2 ? (i = p, s = u) : c >= 2 && c < 3 ? (s = u, a = p) : c >= 3 && c < 4 ? (s = p, a = u) : c >= 4 && c < 5 ? (i = p, a = u) : c >= 5 && c < 6 && (i = u, a = p);
    const f = r - u / 2;
    this.r = W((i + f) * 255), this.g = W((s + f) * 255), this.b = W((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: r,
    a: o
  }) {
    this._h = t % 360, this._s = n, this._v = r, this.a = typeof o == "number" ? o : 1;
    const i = W(r * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, u = W(r * (1 - n) * 255), p = W(r * (1 - n * c) * 255), f = W(r * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = u;
        break;
      case 1:
        this.r = p, this.b = u;
        break;
      case 2:
        this.r = u, this.b = f;
        break;
      case 3:
        this.r = u, this.g = p;
        break;
      case 4:
        this.r = f, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = p;
        break;
    }
  }
  fromHsvString(t) {
    const n = xt(t, En);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = xt(t, En);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = xt(t, (r, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? W(r / 100 * 255) : r
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Ai = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, $i = Object.assign(Object.assign({}, Ai), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Et(e) {
  return e >= 0 && e <= 255;
}
function Ve(e, t) {
  const {
    r: n,
    g: r,
    b: o,
    a: i
  } = new de(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new de(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const p = Math.round((n - s * (1 - u)) / u), f = Math.round((r - a * (1 - u)) / u), d = Math.round((o - c * (1 - u)) / u);
    if (Et(p) && Et(f) && Et(d))
      return new de({
        r: p,
        g: f,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new de({
    r: n,
    g: r,
    b: o,
    a: 1
  }).toRgbString();
}
var ki = function(e, t) {
  var n = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
    t.indexOf(r[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[o]) && (n[r[o]] = e[r[o]]);
  return n;
};
function ji(e) {
  const {
    override: t
  } = e, n = ki(e, ["override"]), r = Object.assign({}, t);
  Object.keys($i).forEach((d) => {
    delete r[d];
  });
  const o = Object.assign(Object.assign({}, n), r), i = 480, s = 576, a = 768, c = 992, u = 1200, p = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: Ve(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: Ve(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: Ve(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: Ve(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: p - 1,
    screenXXL: p,
    screenXXLMin: p,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new de("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new de("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new de("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), r);
}
const Di = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, Ni = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, zi = Ar(ke.defaultAlgorithm), Hi = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, tr = (e, t, n) => {
  const r = n.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...r,
    override: o
  };
  return s = ji(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: u,
      ...p
    } = c;
    let f = p;
    u && (f = tr({
      ...s,
      ...p
    }, {
      override: p
    }, u)), s[a] = f;
  }), s;
};
function Ui() {
  const {
    token: e,
    hashed: t,
    theme: n = zi,
    override: r,
    cssVar: o
  } = l.useContext(ke._internalContext), [i, s, a] = $r(n, [ke.defaultSeed, e], {
    salt: `${Io}-${t || ""}`,
    override: r,
    getComputedToken: tr,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: Di,
      ignore: Ni,
      preserve: Hi
    }
  });
  return [n, a, t ? s : "", i, o];
}
const {
  genStyleHooks: Bi
} = Fi({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Ze();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, r, o] = Ui();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: r,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Ze();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Vi = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list-card`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [r]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${r}-name,${r}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${r}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${r}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${r}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${r}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        [`&:not(${r}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${r}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${r}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${r}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${r}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, kt = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Xi = (e) => {
  const {
    componentCls: t,
    calc: n,
    antCls: r
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...kt,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...kt,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: n(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, Wi = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...kt,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: n(o).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: o,
          height: o,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, Gi = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new de(t).setA(0.85).toRgbString()
  };
}, nr = Bi("Attachments", (e) => {
  const t = Bt(e, {});
  return [Xi(t), Wi(t), Vi(t)];
}, Gi), Ki = (e) => e.indexOf("image/") === 0, Xe = 200;
function qi(e) {
  return new Promise((t) => {
    if (!e || !e.type || !Ki(e.type)) {
      t("");
      return;
    }
    const n = new Image();
    if (n.onload = () => {
      const {
        width: r,
        height: o
      } = n, i = r / o, s = i > 1 ? Xe : Xe * i, a = i > 1 ? Xe / i : Xe, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(n, 0, 0, s, a);
      const p = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(n.src), t(p);
    }, n.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (n.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      n.src = window.URL.createObjectURL(e);
  });
}
function Zi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "audio"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function Qi(e) {
  const {
    percent: t
  } = e, {
    token: n
  } = ke.useToken();
  return /* @__PURE__ */ l.createElement(br, {
    type: "circle",
    percent: t,
    size: n.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ l.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function Yi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "video"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const Ct = " ", jt = "#8c8c8c", rr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Ji = [{
  icon: /* @__PURE__ */ l.createElement(Er, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ l.createElement(Cr, null),
  color: jt,
  ext: rr
}, {
  icon: /* @__PURE__ */ l.createElement(_r, null),
  color: jt,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Rr, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ l.createElement(Lr, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Ir, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Tr, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ l.createElement(Yi, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ l.createElement(Zi, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Cn(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
function es(e) {
  let t = e;
  const n = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < n.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${n[r]}`;
}
function ts(e, t) {
  const {
    prefixCls: n,
    item: r,
    onRemove: o,
    className: i,
    style: s,
    imageProps: a
  } = e, c = l.useContext(De), {
    disabled: u
  } = c || {}, {
    name: p,
    size: f,
    percent: d,
    status: m = "done",
    description: y
  } = r, {
    getPrefixCls: w
  } = Ze(), h = w("attachment", n), b = `${h}-list-card`, [E, C, g] = nr(h), [x, v] = l.useMemo(() => {
    const D = p || "", H = D.match(/^(.*)\.[^.]+$/);
    return H ? [H[1], D.slice(H[1].length)] : [D, ""];
  }, [p]), R = l.useMemo(() => Cn(v, rr), [v]), S = l.useMemo(() => y || (m === "uploading" ? `${d || 0}%` : m === "error" ? r.response || Ct : f ? es(f) : Ct), [m, d]), [T, $] = l.useMemo(() => {
    for (const {
      ext: D,
      icon: H,
      color: Z
    } of Ji)
      if (Cn(v, D))
        return [H, Z];
    return [/* @__PURE__ */ l.createElement(wr, {
      key: "defaultIcon"
    }), jt];
  }, [v]), [j, _] = l.useState();
  l.useEffect(() => {
    if (r.originFileObj) {
      let D = !0;
      return qi(r.originFileObj).then((H) => {
        D && _(H);
      }), () => {
        D = !1;
      };
    }
    _(void 0);
  }, [r.originFileObj]);
  let M = null;
  const P = r.thumbUrl || r.url || j, O = R && (r.originFileObj || P);
  return O ? M = /* @__PURE__ */ l.createElement(l.Fragment, null, P && /* @__PURE__ */ l.createElement(yr, Ie({}, a, {
    alt: "preview",
    src: P
  })), m !== "done" && /* @__PURE__ */ l.createElement("div", {
    className: `${b}-img-mask`
  }, m === "uploading" && d !== void 0 && /* @__PURE__ */ l.createElement(Qi, {
    percent: d,
    prefixCls: b
  }), m === "error" && /* @__PURE__ */ l.createElement("div", {
    className: `${b}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-prefix`
  }, S)))) : M = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-icon`,
    style: {
      color: $
    }
  }, T), /* @__PURE__ */ l.createElement("div", {
    className: `${b}-content`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-name`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-prefix`
  }, x ?? Ct), /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-suffix`
  }, v)), /* @__PURE__ */ l.createElement("div", {
    className: `${b}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${b}-ellipsis-prefix`
  }, S)))), E(/* @__PURE__ */ l.createElement("div", {
    className: oe(b, {
      [`${b}-status-${m}`]: m,
      [`${b}-type-preview`]: O,
      [`${b}-type-overview`]: !O
    }, i, C, g),
    style: s,
    ref: t
  }, M, !u && o && /* @__PURE__ */ l.createElement("button", {
    type: "button",
    className: `${b}-remove`,
    onClick: () => {
      o(r);
    }
  }, /* @__PURE__ */ l.createElement(xr, null))));
}
const or = /* @__PURE__ */ l.forwardRef(ts), _n = 1;
function ns(e) {
  const {
    prefixCls: t,
    items: n,
    onRemove: r,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: u,
    imageProps: p
  } = e, f = `${t}-list`, d = l.useRef(null), [m, y] = l.useState(!1), {
    disabled: w
  } = l.useContext(De);
  l.useEffect(() => (y(!0), () => {
    y(!1);
  }), []);
  const [h, b] = l.useState(!1), [E, C] = l.useState(!1), g = () => {
    const S = d.current;
    S && (o === "scrollX" ? (b(Math.abs(S.scrollLeft) >= _n), C(S.scrollWidth - S.clientWidth - Math.abs(S.scrollLeft) >= _n)) : o === "scrollY" && (b(S.scrollTop !== 0), C(S.scrollHeight - S.clientHeight !== S.scrollTop)));
  };
  l.useEffect(() => {
    g();
  }, [o, n.length]);
  const x = (S) => {
    const T = d.current;
    T && T.scrollTo({
      left: T.scrollLeft + S * T.clientWidth,
      behavior: "smooth"
    });
  }, v = () => {
    x(-1);
  }, R = () => {
    x(1);
  };
  return /* @__PURE__ */ l.createElement("div", {
    className: oe(f, {
      [`${f}-overflow-${e.overflow}`]: o,
      [`${f}-overflow-ping-start`]: h,
      [`${f}-overflow-ping-end`]: E
    }, s),
    ref: d,
    onScroll: g,
    style: a
  }, /* @__PURE__ */ l.createElement(Si, {
    keys: n.map((S) => ({
      key: S.uid,
      item: S
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: m,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: S,
    item: T,
    className: $,
    style: j
  }) => /* @__PURE__ */ l.createElement(or, {
    key: S,
    prefixCls: t,
    item: T,
    onRemove: r,
    className: oe($, c),
    imageProps: p,
    style: {
      ...j,
      ...u
    }
  })), !w && /* @__PURE__ */ l.createElement(Qn, {
    upload: i
  }, /* @__PURE__ */ l.createElement(pt, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ l.createElement(Pr, {
    className: `${f}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(pt, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ l.createElement(Mr, null),
    onClick: v
  }), /* @__PURE__ */ l.createElement(pt, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ l.createElement(Or, null),
    onClick: R
  })));
}
function rs(e, t) {
  const {
    prefixCls: n,
    placeholder: r = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${n}-placeholder`, c = r || {}, {
    disabled: u
  } = l.useContext(De), [p, f] = l.useState(!1), d = () => {
    f(!0);
  }, m = (h) => {
    h.currentTarget.contains(h.relatedTarget) || f(!1);
  }, y = () => {
    f(!1);
  }, w = /* @__PURE__ */ l.isValidElement(r) ? r : /* @__PURE__ */ l.createElement(Sr, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ l.createElement(mt.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ l.createElement(mt.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ l.createElement(mt.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ l.createElement("div", {
    className: oe(a, {
      [`${a}-drag-in`]: p,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: m,
    onDrop: y,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ l.createElement(Ln.Dragger, Ie({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), w));
}
const os = /* @__PURE__ */ l.forwardRef(rs);
function is(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: c,
    getDropContainer: u,
    placeholder: p,
    onChange: f,
    onRemove: d,
    overflow: m,
    imageProps: y,
    disabled: w,
    classNames: h = {},
    styles: b = {},
    ...E
  } = e, {
    getPrefixCls: C,
    direction: g
  } = Ze(), x = C("attachment", n), v = Mo("attachments"), {
    classNames: R,
    styles: S
  } = v, T = l.useRef(null), $ = l.useRef(null);
  l.useImperativeHandle(t, () => ({
    nativeElement: T.current,
    upload: (N) => {
      var z, Q;
      const G = (Q = (z = $.current) == null ? void 0 : z.nativeElement) == null ? void 0 : Q.querySelector('input[type="file"]');
      if (G) {
        const me = new DataTransfer();
        me.items.add(N), G.files = me.files, G.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [j, _, M] = nr(x), P = oe(_, M), [O, D] = jo([], {
    value: a
  }), H = Te((N) => {
    D(N.fileList), f == null || f(N);
  }), Z = {
    ...E,
    fileList: O,
    onChange: H
  }, pe = (N) => Promise.resolve(typeof d == "function" ? d(N) : d).then((G) => {
    if (G === !1)
      return;
    const z = O.filter((Q) => Q.uid !== N.uid);
    H({
      file: {
        ...N,
        status: "removed"
      },
      fileList: z
    });
  });
  let le;
  const V = (N, G, z) => {
    const Q = typeof p == "function" ? p(N) : p;
    return /* @__PURE__ */ l.createElement(os, {
      placeholder: Q,
      upload: Z,
      prefixCls: x,
      className: oe(R.placeholder, h.placeholder),
      style: {
        ...S.placeholder,
        ...b.placeholder,
        ...G == null ? void 0 : G.style
      },
      ref: z
    });
  };
  if (c)
    le = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(Qn, {
      upload: Z,
      rootClassName: r,
      ref: $
    }, c), /* @__PURE__ */ l.createElement(ln, {
      getDropContainer: u,
      prefixCls: x,
      className: oe(P, r)
    }, V("drop")));
  else {
    const N = O.length > 0;
    le = /* @__PURE__ */ l.createElement("div", {
      className: oe(x, P, {
        [`${x}-rtl`]: g === "rtl"
      }, i, r),
      style: {
        ...o,
        ...s
      },
      dir: g || "ltr",
      ref: T
    }, /* @__PURE__ */ l.createElement(ns, {
      prefixCls: x,
      items: O,
      onRemove: pe,
      overflow: m,
      upload: Z,
      listClassName: oe(R.list, h.list),
      listStyle: {
        ...S.list,
        ...b.list,
        ...!N && {
          display: "none"
        }
      },
      itemClassName: oe(R.item, h.item),
      itemStyle: {
        ...S.item,
        ...b.item
      },
      imageProps: y
    }), V("inline", N ? {
      style: {
        display: "none"
      }
    } : {}, $), /* @__PURE__ */ l.createElement(ln, {
      getDropContainer: u || (() => T.current),
      prefixCls: x,
      className: P
    }, V("drop")));
  }
  return j(/* @__PURE__ */ l.createElement(De.Provider, {
    value: {
      disabled: w
    }
  }, le));
}
const ir = /* @__PURE__ */ l.forwardRef(is);
ir.FileCard = or;
function ss(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function as(e, t = !1) {
  try {
    if (mr(e))
      return e;
    if (t && !ss(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function J(e, t) {
  return Ye(() => as(e, t), [e, t]);
}
function ls(e, t) {
  const n = Ye(() => l.Children.toArray(e.originalChildren || e).filter((i) => i.props.node && !i.props.node.ignore && (!i.props.nodeSlotKey || t)).sort((i, s) => {
    if (i.props.node.slotIndex && s.props.node.slotIndex) {
      const a = Ae(i.props.node.slotIndex) || 0, c = Ae(s.props.node.slotIndex) || 0;
      return a - c === 0 && i.props.node.subSlotIndex && s.props.node.subSlotIndex ? (Ae(i.props.node.subSlotIndex) || 0) - (Ae(s.props.node.subSlotIndex) || 0) : a - c;
    }
    return 0;
  }).map((i) => i.props.node.target), [e, t]);
  return Eo(n);
}
function cs(e, t) {
  return Object.keys(e).reduce((n, r) => (e[r] !== void 0 && (n[r] = e[r]), n), {});
}
const us = ({
  children: e,
  ...t
}) => /* @__PURE__ */ te.jsx(te.Fragment, {
  children: e(t)
});
function fs(e) {
  return l.createElement(us, {
    children: e
  });
}
function Rn(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? fs((n) => /* @__PURE__ */ te.jsx(gr, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ te.jsx($e, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ te.jsx($e, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function re({
  key: e,
  slots: t,
  targets: n
}, r) {
  return t[e] ? (...o) => n ? n.map((i, s) => /* @__PURE__ */ te.jsx(l.Fragment, {
    children: Rn(i, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ te.jsx(te.Fragment, {
    children: Rn(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const ds = (e) => !!e.name;
function _t(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const hs = wo(({
  slots: e,
  upload: t,
  showUploadList: n,
  progress: r,
  beforeUpload: o,
  customRequest: i,
  previewFile: s,
  isImageUrl: a,
  itemRender: c,
  iconRender: u,
  data: p,
  onChange: f,
  onValueChange: d,
  onRemove: m,
  items: y,
  setSlotParams: w,
  placeholder: h,
  getDropContainer: b,
  children: E,
  maxCount: C,
  imageProps: g,
  ...x
}) => {
  const v = _t(g == null ? void 0 : g.preview), R = e["imageProps.preview.mask"] || e["imageProps.preview.closeIcon"] || e["imageProps.preview.toolbarRender"] || e["imageProps.preview.imageRender"] || (g == null ? void 0 : g.preview) !== !1, S = J(v.getContainer), T = J(v.toolbarRender), $ = J(v.imageRender), j = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof n == "object", _ = _t(n), M = e["placeholder.title"] || e["placeholder.description"] || e["placeholder.icon"] || typeof h == "object", P = _t(h), O = J(_.showPreviewIcon), D = J(_.showRemoveIcon), H = J(_.showDownloadIcon), {
    token: Z
  } = ke.useToken(), pe = J(o), le = J(i), V = J(r == null ? void 0 : r.format), N = J(s), G = J(a), z = J(c), Q = J(u), me = J(h, !0), se = J(b), Oe = J(p), ce = he(!1), [ue, ge] = Dt(y);
  we(() => {
    ge(y);
  }, [y]);
  const fe = Ye(() => {
    const ne = {};
    return ue.map((X) => {
      if (!ds(X)) {
        const B = X.uid || X.url || X.path;
        return ne[B] || (ne[B] = 0), ne[B]++, {
          ...X,
          name: X.orig_name || X.path,
          uid: X.uid || B + "-" + ne[B],
          status: "done"
        };
      }
      return X;
    }) || [];
  }, [ue]), be = ls(E);
  return /* @__PURE__ */ te.jsxs(te.Fragment, {
    children: [/* @__PURE__ */ te.jsx("div", {
      style: {
        display: "none"
      },
      children: be.length > 0 ? null : E
    }), /* @__PURE__ */ te.jsx(ir, {
      ...x,
      imageProps: {
        ...g,
        preview: R ? cs({
          ...v,
          getContainer: S,
          toolbarRender: e["imageProps.preview.toolbarRender"] ? re({
            slots: e,
            key: "imageProps.preview.toolbarRender"
          }) : T,
          imageRender: e["imageProps.preview.imageRender"] ? re({
            slots: e,
            key: "imageProps.preview.imageRender"
          }) : $,
          ...e["imageProps.preview.mask"] || Reflect.has(v, "mask") ? {
            mask: e["imageProps.preview.mask"] ? /* @__PURE__ */ te.jsx($e, {
              slot: e["imageProps.preview.mask"]
            }) : v.mask
          } : {},
          closeIcon: e["imageProps.preview.closeIcon"] ? /* @__PURE__ */ te.jsx($e, {
            slot: e["imageProps.preview.closeIcon"]
          }) : v.closeIcon
        }) : !1,
        placeholder: e["imageProps.placeholder"] ? /* @__PURE__ */ te.jsx($e, {
          slot: e["imageProps.placeholder"]
        }) : g == null ? void 0 : g.placeholder,
        wrapperStyle: {
          width: "100%",
          height: "100%",
          ...g == null ? void 0 : g.wrapperStyle
        },
        style: {
          width: "100%",
          height: "100%",
          objectFit: "contain",
          borderRadius: Z.borderRadius,
          ...g == null ? void 0 : g.style
        }
      },
      getDropContainer: se,
      placeholder: e.placeholder ? re({
        slots: e,
        key: "placeholder"
      }) : M ? (...ne) => {
        var X, B, ye;
        return {
          ...P,
          icon: e["placeholder.icon"] ? (X = re({
            slots: e,
            key: "placeholder.icon"
          })) == null ? void 0 : X(...ne) : P.icon,
          title: e["placeholder.title"] ? (B = re({
            slots: e,
            key: "placeholder.title"
          })) == null ? void 0 : B(...ne) : P.title,
          description: e["placeholder.description"] ? (ye = re({
            slots: e,
            key: "placeholder.description"
          })) == null ? void 0 : ye(...ne) : P.description
        };
      } : me || h,
      items: fe,
      data: Oe || p,
      previewFile: N,
      isImageUrl: G,
      itemRender: e.itemRender ? re({
        slots: e,
        key: "itemRender"
      }) : z,
      iconRender: e.iconRender ? re({
        slots: e,
        key: "iconRender"
      }) : Q,
      maxCount: C,
      onChange: async (ne) => {
        const X = ne.file, B = ne.fileList, ye = fe.findIndex((Y) => Y.uid === X.uid);
        if (ye !== -1) {
          if (ce.current)
            return;
          m == null || m(X);
          const Y = ue.slice();
          Y.splice(ye, 1), d == null || d(Y), f == null || f(Y.map((Se) => Se.path));
        } else {
          if (pe && !await pe(X, B) || ce.current)
            return;
          ce.current = !0;
          let Y = B.filter((k) => k.status !== "done");
          if (C === 1)
            Y = Y.slice(0, 1);
          else if (Y.length === 0) {
            ce.current = !1;
            return;
          } else if (typeof C == "number") {
            const k = C - ue.length;
            Y = Y.slice(0, k < 0 ? 0 : k);
          }
          const Se = ue, Ee = Y.map((k) => ({
            ...k,
            size: k.size,
            uid: k.uid,
            name: k.name,
            status: "uploading"
          }));
          ge((k) => [...C === 1 ? [] : k, ...Ee]);
          const K = (await t(Y.map((k) => k.originFileObj))).filter(Boolean).map((k, Ce) => ({
            ...k,
            uid: Ee[Ce].uid
          })), U = C === 1 ? K : [...Se, ...K];
          ce.current = !1, ge(U), d == null || d(U), f == null || f(U.map((k) => k.path));
        }
      },
      customRequest: le || Vr,
      progress: r && {
        ...r,
        format: V
      },
      showUploadList: j ? {
        ..._,
        showDownloadIcon: H || _.showDownloadIcon,
        showRemoveIcon: D || _.showRemoveIcon,
        showPreviewIcon: O || _.showPreviewIcon,
        downloadIcon: e["showUploadList.downloadIcon"] ? re({
          slots: e,
          key: "showUploadList.downloadIcon"
        }) : _.downloadIcon,
        removeIcon: e["showUploadList.removeIcon"] ? re({
          slots: e,
          key: "showUploadList.removeIcon"
        }) : _.removeIcon,
        previewIcon: e["showUploadList.previewIcon"] ? re({
          slots: e,
          key: "showUploadList.previewIcon"
        }) : _.previewIcon,
        extra: e["showUploadList.extra"] ? re({
          slots: e,
          key: "showUploadList.extra"
        }) : _.extra
      } : n,
      children: be.length > 0 ? E : void 0
    })]
  });
});
export {
  hs as Attachments,
  hs as default
};

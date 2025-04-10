import { i as br, a as _t, r as Sr, b as xr, w as We, g as Cr, c as te, d as Er } from "./Index-BCJ9URxB.js";
const p = window.ms_globals.React, y = window.ms_globals.React, dr = window.ms_globals.React.forwardRef, re = window.ms_globals.React.useRef, On = window.ms_globals.React.useState, pe = window.ms_globals.React.useEffect, hr = window.ms_globals.React.version, mr = window.ms_globals.React.isValidElement, pr = window.ms_globals.React.useLayoutEffect, gr = window.ms_globals.React.useImperativeHandle, vr = window.ms_globals.React.memo, yr = window.ms_globals.React.useMemo, zt = window.ms_globals.ReactDOM, wt = window.ms_globals.ReactDOM.createPortal, wr = window.ms_globals.internalContext.useContextPropsContext, _r = window.ms_globals.internalContext.ContextPropsProvider, Tr = window.ms_globals.internalContext.useSuggestionOpenContext, Rr = window.ms_globals.antd.ConfigProvider, Tt = window.ms_globals.antd.theme, An = window.ms_globals.antd.Button, Pr = window.ms_globals.antd.Input, Mr = window.ms_globals.antd.Flex, Or = window.ms_globals.antdIcons.CloseOutlined, Ar = window.ms_globals.antdIcons.ClearOutlined, kr = window.ms_globals.antdIcons.ArrowUpOutlined, Lr = window.ms_globals.antdIcons.AudioMutedOutlined, Ir = window.ms_globals.antdIcons.AudioOutlined, Rt = window.ms_globals.antdCssinjs.unit, pt = window.ms_globals.antdCssinjs.token2CSSVar, Xt = window.ms_globals.antdCssinjs.useStyleRegister, jr = window.ms_globals.antdCssinjs.useCSSVarRegister, $r = window.ms_globals.antdCssinjs.createTheme, Dr = window.ms_globals.antdCssinjs.useCacheToken;
var Nr = /\s/;
function Br(e) {
  for (var t = e.length; t-- && Nr.test(e.charAt(t)); )
    ;
  return t;
}
var Hr = /^\s+/;
function Vr(e) {
  return e && e.slice(0, Br(e) + 1).replace(Hr, "");
}
var Ut = NaN, Fr = /^[-+]0x[0-9a-f]+$/i, zr = /^0b[01]+$/i, Xr = /^0o[0-7]+$/i, Ur = parseInt;
function Wt(e) {
  if (typeof e == "number")
    return e;
  if (br(e))
    return Ut;
  if (_t(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = _t(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Vr(e);
  var n = zr.test(e);
  return n || Xr.test(e) ? Ur(e.slice(2), n ? 2 : 8) : Fr.test(e) ? Ut : +e;
}
var gt = function() {
  return Sr.Date.now();
}, Wr = "Expected a function", Kr = Math.max, Gr = Math.min;
function qr(e, t, n) {
  var o, r, i, s, a, c, l = 0, f = !1, u = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Wr);
  t = Wt(t) || 0, _t(n) && (f = !!n.leading, u = "maxWait" in n, i = u ? Kr(Wt(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function h(S) {
    var T = o, P = r;
    return o = r = void 0, l = S, s = e.apply(P, T), s;
  }
  function v(S) {
    return l = S, a = setTimeout(x, t), f ? h(S) : s;
  }
  function g(S) {
    var T = S - c, P = S - l, k = t - T;
    return u ? Gr(k, i - P) : k;
  }
  function m(S) {
    var T = S - c, P = S - l;
    return c === void 0 || T >= t || T < 0 || u && P >= i;
  }
  function x() {
    var S = gt();
    if (m(S))
      return C(S);
    a = setTimeout(x, g(S));
  }
  function C(S) {
    return a = void 0, d && o ? h(S) : (o = r = void 0, s);
  }
  function _() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = r = a = void 0;
  }
  function b() {
    return a === void 0 ? s : C(gt());
  }
  function R() {
    var S = gt(), T = m(S);
    if (o = arguments, r = this, c = S, T) {
      if (a === void 0)
        return v(c);
      if (u)
        return clearTimeout(a), a = setTimeout(x, t), h(c);
    }
    return a === void 0 && (a = setTimeout(x, t)), s;
  }
  return R.cancel = _, R.flush = b, R;
}
function Qr(e, t) {
  return xr(e, t);
}
var kn = {
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
var Yr = y, Zr = Symbol.for("react.element"), Jr = Symbol.for("react.fragment"), eo = Object.prototype.hasOwnProperty, to = Yr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, no = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Ln(e, t, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) eo.call(t, o) && !no.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: Zr,
    type: e,
    key: i,
    ref: s,
    props: r,
    _owner: to.current
  };
}
Je.Fragment = Jr;
Je.jsx = Ln;
Je.jsxs = Ln;
kn.exports = Je;
var q = kn.exports;
const {
  SvelteComponent: ro,
  assign: Kt,
  binding_callbacks: Gt,
  check_outros: oo,
  children: In,
  claim_element: jn,
  claim_space: io,
  component_subscribe: qt,
  compute_slots: so,
  create_slot: ao,
  detach: Ce,
  element: $n,
  empty: Qt,
  exclude_internal_props: Yt,
  get_all_dirty_from_scope: co,
  get_slot_changes: lo,
  group_outros: uo,
  init: fo,
  insert_hydration: Ke,
  safe_not_equal: ho,
  set_custom_element_data: Dn,
  space: mo,
  transition_in: Ge,
  transition_out: Pt,
  update_slot_base: po
} = window.__gradio__svelte__internal, {
  beforeUpdate: go,
  getContext: vo,
  onDestroy: yo,
  setContext: bo
} = window.__gradio__svelte__internal;
function Zt(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = ao(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = $n("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      t = jn(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = In(t);
      r && r.l(s), s.forEach(Ce), this.h();
    },
    h() {
      Dn(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ke(i, t, s), r && r.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && po(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? lo(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : co(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (Ge(r, i), n = !0);
    },
    o(i) {
      Pt(r, i), n = !1;
    },
    d(i) {
      i && Ce(t), r && r.d(i), e[9](null);
    }
  };
}
function So(e) {
  let t, n, o, r, i = (
    /*$$slots*/
    e[4].default && Zt(e)
  );
  return {
    c() {
      t = $n("react-portal-target"), n = mo(), i && i.c(), o = Qt(), this.h();
    },
    l(s) {
      t = jn(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), In(t).forEach(Ce), n = io(s), i && i.l(s), o = Qt(), this.h();
    },
    h() {
      Dn(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ke(s, t, a), e[8](t), Ke(s, n, a), i && i.m(s, a), Ke(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Ge(i, 1)) : (i = Zt(s), i.c(), Ge(i, 1), i.m(o.parentNode, o)) : i && (uo(), Pt(i, 1, 1, () => {
        i = null;
      }), oo());
    },
    i(s) {
      r || (Ge(i), r = !0);
    },
    o(s) {
      Pt(i), r = !1;
    },
    d(s) {
      s && (Ce(t), Ce(n), Ce(o)), e[8](null), i && i.d(s);
    }
  };
}
function Jt(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function xo(e, t, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = so(i);
  let {
    svelteInit: c
  } = t;
  const l = We(Jt(t)), f = We();
  qt(e, f, (b) => n(0, o = b));
  const u = We();
  qt(e, u, (b) => n(1, r = b));
  const d = [], h = vo("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: g,
    subSlotIndex: m
  } = Cr() || {}, x = c({
    parent: h,
    props: l,
    target: f,
    slot: u,
    slotKey: v,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(b) {
      d.push(b);
    }
  });
  bo("$$ms-gr-react-wrapper", x), go(() => {
    l.set(Jt(t));
  }), yo(() => {
    d.forEach((b) => b());
  });
  function C(b) {
    Gt[b ? "unshift" : "push"](() => {
      o = b, f.set(o);
    });
  }
  function _(b) {
    Gt[b ? "unshift" : "push"](() => {
      r = b, u.set(r);
    });
  }
  return e.$$set = (b) => {
    n(17, t = Kt(Kt({}, t), Yt(b))), "svelteInit" in b && n(5, c = b.svelteInit), "$$scope" in b && n(6, s = b.$$scope);
  }, t = Yt(t), [o, r, f, u, a, c, s, i, C, _];
}
class Co extends ro {
  constructor(t) {
    super(), fo(this, t, xo, So, ho, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: gs
} = window.__gradio__svelte__internal, en = window.ms_globals.rerender, vt = window.ms_globals.tree;
function Eo(e, t = {}) {
  function n(o) {
    const r = We(), i = new Co({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
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
          return c.nodes = [...c.nodes, a], en({
            createPortal: wt,
            node: vt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== r), en({
              createPortal: wt,
              node: vt
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const wo = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function _o(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = To(n, o), t;
  }, {}) : {};
}
function To(e, t) {
  return typeof t == "number" && !wo.includes(e) ? t + "px" : t;
}
function Mt(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = y.Children.toArray(e._reactElement.props.children).map((i) => {
      if (y.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Mt(i.props.el);
        return y.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...y.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(wt(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, s, c);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Mt(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Ro(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Qe = dr(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = re(), [a, c] = On([]), {
    forceClone: l
  } = wr(), f = l ? !0 : t;
  return pe(() => {
    var g;
    if (!s.current || !e)
      return;
    let u = e;
    function d() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Ro(i, m), n && m.classList.add(...n.split(" ")), o) {
        const x = _o(o);
        Object.keys(x).forEach((C) => {
          m.style[C] = x[C];
        });
      }
    }
    let h = null, v = null;
    if (f && window.MutationObserver) {
      let m = function() {
        var b, R, S;
        (b = s.current) != null && b.contains(u) && ((R = s.current) == null || R.removeChild(u));
        const {
          portals: C,
          clonedElement: _
        } = Mt(e);
        u = _, c(C), u.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (S = s.current) == null || S.appendChild(u);
      };
      m();
      const x = qr(() => {
        m(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      h = new window.MutationObserver(x), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (g = s.current) == null || g.appendChild(u);
    return () => {
      var m, x;
      u.style.display = "", (m = s.current) != null && m.contains(u) && ((x = s.current) == null || x.removeChild(u)), h == null || h.disconnect();
    };
  }, [e, f, n, o, i, r, l]), y.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Po = "1.1.0", Mo = /* @__PURE__ */ y.createContext({}), Oo = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Ao = (e) => {
  const t = y.useContext(Mo);
  return y.useMemo(() => ({
    ...Oo,
    ...t[e]
  }), [t[e]]);
};
function le() {
  return le = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (e[o] = n[o]);
    }
    return e;
  }, le.apply(null, arguments);
}
function Ot() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = y.useContext(Rr.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function ve(e) {
  var t = p.useRef();
  t.current = e;
  var n = p.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(i));
  }, []);
  return n;
}
function ko(e) {
  if (Array.isArray(e)) return e;
}
function Lo(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], c = !0, l = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (o = i.call(n)).done) && (a.push(o.value), a.length !== t); c = !0) ;
    } catch (f) {
      l = !0, r = f;
    } finally {
      try {
        if (!c && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw r;
      }
    }
    return a;
  }
}
function tn(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function Io(e, t) {
  if (e) {
    if (typeof e == "string") return tn(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? tn(e, t) : void 0;
  }
}
function jo() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function W(e, t) {
  return ko(e) || Lo(e, t) || Io(e, t) || jo();
}
function et() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var nn = et() ? p.useLayoutEffect : p.useEffect, $o = function(t, n) {
  var o = p.useRef(!0);
  nn(function() {
    return t(o.current);
  }, n), nn(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, rn = function(t, n) {
  $o(function(o) {
    if (!o)
      return t();
  }, n);
};
function $e(e) {
  var t = p.useRef(!1), n = p.useState(e), o = W(n, 2), r = o[0], i = o[1];
  p.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [r, s];
}
function yt(e) {
  return e !== void 0;
}
function Nn(e, t) {
  var n = t || {}, o = n.defaultValue, r = n.value, i = n.onChange, s = n.postState, a = $e(function() {
    return yt(r) ? r : yt(o) ? typeof o == "function" ? o() : o : typeof e == "function" ? e() : e;
  }), c = W(a, 2), l = c[0], f = c[1], u = r !== void 0 ? r : l, d = s ? s(u) : u, h = ve(i), v = $e([u]), g = W(v, 2), m = g[0], x = g[1];
  rn(function() {
    var _ = m[0];
    l !== _ && h(l, _);
  }, [m]), rn(function() {
    yt(r) || f(r);
  }, [r]);
  var C = ve(function(_, b) {
    f(_, b), x([u], b);
  });
  return [d, C];
}
function V(e) {
  "@babel/helpers - typeof";
  return V = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, V(e);
}
var Bn = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Nt = Symbol.for("react.element"), Bt = Symbol.for("react.portal"), tt = Symbol.for("react.fragment"), nt = Symbol.for("react.strict_mode"), rt = Symbol.for("react.profiler"), ot = Symbol.for("react.provider"), it = Symbol.for("react.context"), Do = Symbol.for("react.server_context"), st = Symbol.for("react.forward_ref"), at = Symbol.for("react.suspense"), ct = Symbol.for("react.suspense_list"), lt = Symbol.for("react.memo"), ut = Symbol.for("react.lazy"), No = Symbol.for("react.offscreen"), Hn;
Hn = Symbol.for("react.module.reference");
function Y(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Nt:
        switch (e = e.type, e) {
          case tt:
          case rt:
          case nt:
          case at:
          case ct:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Do:
              case it:
              case st:
              case ut:
              case lt:
              case ot:
                return e;
              default:
                return t;
            }
        }
      case Bt:
        return t;
    }
  }
}
O.ContextConsumer = it;
O.ContextProvider = ot;
O.Element = Nt;
O.ForwardRef = st;
O.Fragment = tt;
O.Lazy = ut;
O.Memo = lt;
O.Portal = Bt;
O.Profiler = rt;
O.StrictMode = nt;
O.Suspense = at;
O.SuspenseList = ct;
O.isAsyncMode = function() {
  return !1;
};
O.isConcurrentMode = function() {
  return !1;
};
O.isContextConsumer = function(e) {
  return Y(e) === it;
};
O.isContextProvider = function(e) {
  return Y(e) === ot;
};
O.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Nt;
};
O.isForwardRef = function(e) {
  return Y(e) === st;
};
O.isFragment = function(e) {
  return Y(e) === tt;
};
O.isLazy = function(e) {
  return Y(e) === ut;
};
O.isMemo = function(e) {
  return Y(e) === lt;
};
O.isPortal = function(e) {
  return Y(e) === Bt;
};
O.isProfiler = function(e) {
  return Y(e) === rt;
};
O.isStrictMode = function(e) {
  return Y(e) === nt;
};
O.isSuspense = function(e) {
  return Y(e) === at;
};
O.isSuspenseList = function(e) {
  return Y(e) === ct;
};
O.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === tt || e === rt || e === nt || e === at || e === ct || e === No || typeof e == "object" && e !== null && (e.$$typeof === ut || e.$$typeof === lt || e.$$typeof === ot || e.$$typeof === it || e.$$typeof === st || e.$$typeof === Hn || e.getModuleId !== void 0);
};
O.typeOf = Y;
Bn.exports = O;
var bt = Bn.exports, Bo = Symbol.for("react.element"), Ho = Symbol.for("react.transitional.element"), Vo = Symbol.for("react.fragment");
function Fo(e) {
  return (
    // Base object type
    e && V(e) === "object" && // React Element type
    (e.$$typeof === Bo || e.$$typeof === Ho) && // React Fragment type
    e.type === Vo
  );
}
var zo = Number(hr.split(".")[0]), Xo = function(t, n) {
  typeof t == "function" ? t(n) : V(t) === "object" && t && "current" in t && (t.current = n);
}, Uo = function(t) {
  var n, o;
  if (!t)
    return !1;
  if (Vn(t) && zo >= 19)
    return !0;
  var r = bt.isMemo(t) ? t.type.type : t.type;
  return !(typeof r == "function" && !((n = r.prototype) !== null && n !== void 0 && n.render) && r.$$typeof !== bt.ForwardRef || typeof t == "function" && !((o = t.prototype) !== null && o !== void 0 && o.render) && t.$$typeof !== bt.ForwardRef);
};
function Vn(e) {
  return /* @__PURE__ */ mr(e) && !Fo(e);
}
var Wo = function(t) {
  if (t && Vn(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function Ko(e, t) {
  for (var n = e, o = 0; o < t.length; o += 1) {
    if (n == null)
      return;
    n = n[t[o]];
  }
  return n;
}
function Go(e, t) {
  if (V(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t);
    if (V(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Fn(e) {
  var t = Go(e, "string");
  return V(t) == "symbol" ? t : t + "";
}
function w(e, t, n) {
  return (t = Fn(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function on(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function E(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? on(Object(n), !0).forEach(function(o) {
      w(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : on(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function sn(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function qo(e) {
  return e && V(e) === "object" && sn(e.nativeElement) ? e.nativeElement : sn(e) ? e : null;
}
function Qo(e) {
  var t = qo(e);
  if (t)
    return t;
  if (e instanceof y.Component) {
    var n;
    return (n = zt.findDOMNode) === null || n === void 0 ? void 0 : n.call(zt, e);
  }
  return null;
}
function Yo(e, t) {
  if (e == null) return {};
  var n = {};
  for (var o in e) if ({}.hasOwnProperty.call(e, o)) {
    if (t.indexOf(o) !== -1) continue;
    n[o] = e[o];
  }
  return n;
}
function an(e, t) {
  if (e == null) return {};
  var n, o, r = Yo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (o = 0; o < i.length; o++) n = i[o], t.indexOf(n) === -1 && {}.propertyIsEnumerable.call(e, n) && (r[n] = e[n]);
  }
  return r;
}
var Zo = /* @__PURE__ */ p.createContext({});
function _e(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function cn(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Fn(o.key), o);
  }
}
function Te(e, t, n) {
  return t && cn(e.prototype, t), n && cn(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function At(e, t) {
  return At = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, At(e, t);
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
  }), t && At(e, t);
}
function Ye(e) {
  return Ye = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Ye(e);
}
function zn() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (zn = function() {
    return !!e;
  })();
}
function ge(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Jo(e, t) {
  if (t && (V(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ge(e);
}
function dt(e) {
  var t = zn();
  return function() {
    var n, o = Ye(e);
    if (t) {
      var r = Ye(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return Jo(this, n);
  };
}
var ei = /* @__PURE__ */ function(e) {
  ft(n, e);
  var t = dt(n);
  function n() {
    return _e(this, n), t.apply(this, arguments);
  }
  return Te(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(p.Component);
function ti(e) {
  var t = p.useReducer(function(a) {
    return a + 1;
  }, 0), n = W(t, 2), o = n[1], r = p.useRef(e), i = ve(function() {
    return r.current;
  }), s = ve(function(a) {
    r.current = typeof a == "function" ? a(r.current) : a, o();
  });
  return [i, s];
}
var ue = "none", Be = "appear", He = "enter", Ve = "leave", ln = "none", ee = "prepare", Ee = "start", we = "active", Ht = "end", Xn = "prepared";
function un(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function ni(e, t) {
  var n = {
    animationend: un("Animation", "AnimationEnd"),
    transitionend: un("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var ri = ni(et(), typeof window < "u" ? window : {}), Un = {};
if (et()) {
  var oi = document.createElement("div");
  Un = oi.style;
}
var Fe = {};
function Wn(e) {
  if (Fe[e])
    return Fe[e];
  var t = ri[e];
  if (t)
    for (var n = Object.keys(t), o = n.length, r = 0; r < o; r += 1) {
      var i = n[r];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Un)
        return Fe[e] = t[i], Fe[e];
    }
  return "";
}
var Kn = Wn("animationend"), Gn = Wn("transitionend"), qn = !!(Kn && Gn), fn = Kn || "animationend", dn = Gn || "transitionend";
function hn(e, t) {
  if (!e) return null;
  if (V(e) === "object") {
    var n = t.replace(/-\w/g, function(o) {
      return o[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const ii = function(e) {
  var t = re();
  function n(r) {
    r && (r.removeEventListener(dn, e), r.removeEventListener(fn, e));
  }
  function o(r) {
    t.current && t.current !== r && n(t.current), r && r !== t.current && (r.addEventListener(dn, e), r.addEventListener(fn, e), t.current = r);
  }
  return p.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [o, n];
};
var Qn = et() ? pr : pe, Yn = function(t) {
  return +setTimeout(t, 16);
}, Zn = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Yn = function(t) {
  return window.requestAnimationFrame(t);
}, Zn = function(t) {
  return window.cancelAnimationFrame(t);
});
var mn = 0, Vt = /* @__PURE__ */ new Map();
function Jn(e) {
  Vt.delete(e);
}
var kt = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  mn += 1;
  var o = mn;
  function r(i) {
    if (i === 0)
      Jn(o), t();
    else {
      var s = Yn(function() {
        r(i - 1);
      });
      Vt.set(o, s);
    }
  }
  return r(n), o;
};
kt.cancel = function(e) {
  var t = Vt.get(e);
  return Jn(e), Zn(t);
};
const si = function() {
  var e = p.useRef(null);
  function t() {
    kt.cancel(e.current);
  }
  function n(o) {
    var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = kt(function() {
      r <= 1 ? o({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(o, r - 1);
    });
    e.current = i;
  }
  return p.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var ai = [ee, Ee, we, Ht], ci = [ee, Xn], er = !1, li = !0;
function tr(e) {
  return e === we || e === Ht;
}
const ui = function(e, t, n) {
  var o = $e(ln), r = W(o, 2), i = r[0], s = r[1], a = si(), c = W(a, 2), l = c[0], f = c[1];
  function u() {
    s(ee, !0);
  }
  var d = t ? ci : ai;
  return Qn(function() {
    if (i !== ln && i !== Ht) {
      var h = d.indexOf(i), v = d[h + 1], g = n(i);
      g === er ? s(v, !0) : v && l(function(m) {
        function x() {
          m.isCanceled() || s(v, !0);
        }
        g === !0 ? x() : Promise.resolve(g).then(x);
      });
    }
  }, [e, i]), p.useEffect(function() {
    return function() {
      f();
    };
  }, []), [u, i];
};
function fi(e, t, n, o) {
  var r = o.motionEnter, i = r === void 0 ? !0 : r, s = o.motionAppear, a = s === void 0 ? !0 : s, c = o.motionLeave, l = c === void 0 ? !0 : c, f = o.motionDeadline, u = o.motionLeaveImmediately, d = o.onAppearPrepare, h = o.onEnterPrepare, v = o.onLeavePrepare, g = o.onAppearStart, m = o.onEnterStart, x = o.onLeaveStart, C = o.onAppearActive, _ = o.onEnterActive, b = o.onLeaveActive, R = o.onAppearEnd, S = o.onEnterEnd, T = o.onLeaveEnd, P = o.onVisibleChanged, k = $e(), $ = W(k, 2), D = $[0], A = $[1], L = ti(ue), j = W(L, 2), M = j[0], F = j[1], Q = $e(null), N = W(Q, 2), fe = N[0], ye = N[1], K = M(), oe = re(!1), de = re(null);
  function G() {
    return n();
  }
  var ne = re(!1);
  function Z() {
    F(ue), ye(null, !0);
  }
  var J = ve(function(z) {
    var B = M();
    if (B !== ue) {
      var X = G();
      if (!(z && !z.deadline && z.target !== X)) {
        var xe = ne.current, ae;
        B === Be && xe ? ae = R == null ? void 0 : R(X, z) : B === He && xe ? ae = S == null ? void 0 : S(X, z) : B === Ve && xe && (ae = T == null ? void 0 : T(X, z)), xe && ae !== !1 && Z();
      }
    }
  }), he = ii(J), be = W(he, 1), me = be[0], Se = function(B) {
    switch (B) {
      case Be:
        return w(w(w({}, ee, d), Ee, g), we, C);
      case He:
        return w(w(w({}, ee, h), Ee, m), we, _);
      case Ve:
        return w(w(w({}, ee, v), Ee, x), we, b);
      default:
        return {};
    }
  }, ie = p.useMemo(function() {
    return Se(K);
  }, [K]), Re = ui(K, !e, function(z) {
    if (z === ee) {
      var B = ie[ee];
      return B ? B(G()) : er;
    }
    if (se in ie) {
      var X;
      ye(((X = ie[se]) === null || X === void 0 ? void 0 : X.call(ie, G(), null)) || null);
    }
    return se === we && K !== ue && (me(G()), f > 0 && (clearTimeout(de.current), de.current = setTimeout(function() {
      J({
        deadline: !0
      });
    }, f))), se === Xn && Z(), li;
  }), De = W(Re, 2), Pe = De[0], se = De[1], Me = tr(se);
  ne.current = Me;
  var Ne = re(null);
  Qn(function() {
    if (!(oe.current && Ne.current === t)) {
      A(t);
      var z = oe.current;
      oe.current = !0;
      var B;
      !z && t && a && (B = Be), z && t && i && (B = He), (z && !t && l || !z && u && !t && l) && (B = Ve);
      var X = Se(B);
      B && (e || X[ee]) ? (F(B), Pe()) : F(ue), Ne.current = t;
    }
  }, [t]), pe(function() {
    // Cancel appear
    (K === Be && !a || // Cancel enter
    K === He && !i || // Cancel leave
    K === Ve && !l) && F(ue);
  }, [a, i, l]), pe(function() {
    return function() {
      oe.current = !1, clearTimeout(de.current);
    };
  }, []);
  var Oe = p.useRef(!1);
  pe(function() {
    D && (Oe.current = !0), D !== void 0 && K === ue && ((Oe.current || D) && (P == null || P(D)), Oe.current = !0);
  }, [D, K]);
  var Ae = fe;
  return ie[ee] && se === Ee && (Ae = E({
    transition: "none"
  }, Ae)), [K, se, Ae, D ?? t];
}
function di(e) {
  var t = e;
  V(e) === "object" && (t = e.transitionSupport);
  function n(r, i) {
    return !!(r.motionName && t && i !== !1);
  }
  var o = /* @__PURE__ */ p.forwardRef(function(r, i) {
    var s = r.visible, a = s === void 0 ? !0 : s, c = r.removeOnLeave, l = c === void 0 ? !0 : c, f = r.forceRender, u = r.children, d = r.motionName, h = r.leavedClassName, v = r.eventProps, g = p.useContext(Zo), m = g.motion, x = n(r, m), C = re(), _ = re();
    function b() {
      try {
        return C.current instanceof HTMLElement ? C.current : Qo(_.current);
      } catch {
        return null;
      }
    }
    var R = fi(x, a, b, r), S = W(R, 4), T = S[0], P = S[1], k = S[2], $ = S[3], D = p.useRef($);
    $ && (D.current = !0);
    var A = p.useCallback(function(N) {
      C.current = N, Xo(i, N);
    }, [i]), L, j = E(E({}, v), {}, {
      visible: a
    });
    if (!u)
      L = null;
    else if (T === ue)
      $ ? L = u(E({}, j), A) : !l && D.current && h ? L = u(E(E({}, j), {}, {
        className: h
      }), A) : f || !l && !h ? L = u(E(E({}, j), {}, {
        style: {
          display: "none"
        }
      }), A) : L = null;
    else {
      var M;
      P === ee ? M = "prepare" : tr(P) ? M = "active" : P === Ee && (M = "start");
      var F = hn(d, "".concat(T, "-").concat(M));
      L = u(E(E({}, j), {}, {
        className: te(hn(d, T), w(w({}, F, F && M), d, typeof d == "string")),
        style: k
      }), A);
    }
    if (/* @__PURE__ */ p.isValidElement(L) && Uo(L)) {
      var Q = Wo(L);
      Q || (L = /* @__PURE__ */ p.cloneElement(L, {
        ref: A
      }));
    }
    return /* @__PURE__ */ p.createElement(ei, {
      ref: _
    }, L);
  });
  return o.displayName = "CSSMotion", o;
}
const nr = di(qn);
var Lt = "add", It = "keep", jt = "remove", St = "removed";
function hi(e) {
  var t;
  return e && V(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, E(E({}, t), {}, {
    key: String(t.key)
  });
}
function $t() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(hi);
}
function mi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], o = 0, r = t.length, i = $t(e), s = $t(t);
  i.forEach(function(l) {
    for (var f = !1, u = o; u < r; u += 1) {
      var d = s[u];
      if (d.key === l.key) {
        o < u && (n = n.concat(s.slice(o, u).map(function(h) {
          return E(E({}, h), {}, {
            status: Lt
          });
        })), o = u), n.push(E(E({}, d), {}, {
          status: It
        })), o += 1, f = !0;
        break;
      }
    }
    f || n.push(E(E({}, l), {}, {
      status: jt
    }));
  }), o < r && (n = n.concat(s.slice(o).map(function(l) {
    return E(E({}, l), {}, {
      status: Lt
    });
  })));
  var a = {};
  n.forEach(function(l) {
    var f = l.key;
    a[f] = (a[f] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(l) {
    return a[l] > 1;
  });
  return c.forEach(function(l) {
    n = n.filter(function(f) {
      var u = f.key, d = f.status;
      return u !== l || d !== jt;
    }), n.forEach(function(f) {
      f.key === l && (f.status = It);
    });
  }), n;
}
var pi = ["component", "children", "onVisibleChanged", "onAllRemoved"], gi = ["status"], vi = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function yi(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : nr, n = /* @__PURE__ */ function(o) {
    ft(i, o);
    var r = dt(i);
    function i() {
      var s;
      _e(this, i);
      for (var a = arguments.length, c = new Array(a), l = 0; l < a; l++)
        c[l] = arguments[l];
      return s = r.call.apply(r, [this].concat(c)), w(ge(s), "state", {
        keyEntities: []
      }), w(ge(s), "removeKey", function(f) {
        s.setState(function(u) {
          var d = u.keyEntities.map(function(h) {
            return h.key !== f ? h : E(E({}, h), {}, {
              status: St
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var u = s.state.keyEntities, d = u.filter(function(h) {
            var v = h.status;
            return v !== St;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Te(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, l = this.props, f = l.component, u = l.children, d = l.onVisibleChanged;
        l.onAllRemoved;
        var h = an(l, pi), v = f || p.Fragment, g = {};
        return vi.forEach(function(m) {
          g[m] = h[m], delete h[m];
        }), delete h.keys, /* @__PURE__ */ p.createElement(v, h, c.map(function(m, x) {
          var C = m.status, _ = an(m, gi), b = C === Lt || C === It;
          return /* @__PURE__ */ p.createElement(t, le({}, g, {
            key: _.key,
            visible: b,
            eventProps: _,
            onVisibleChanged: function(S) {
              d == null || d(S, {
                key: _.key
              }), S || a.removeKey(_.key);
            }
          }), function(R, S) {
            return u(E(E({}, R), {}, {
              index: x
            }), S);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var l = a.keys, f = c.keyEntities, u = $t(l), d = mi(f, u);
        return {
          keyEntities: d.filter(function(h) {
            var v = f.find(function(g) {
              var m = g.key;
              return h.key === m;
            });
            return !(v && v.status === St && h.status === jt);
          })
        };
      }
    }]), i;
  }(p.Component);
  return w(n, "defaultProps", {
    component: "div"
  }), n;
}
yi(qn);
var rr = /* @__PURE__ */ Te(function e() {
  _e(this, e);
}), or = "CALC_UNIT", bi = new RegExp(or, "g");
function xt(e) {
  return typeof e == "number" ? "".concat(e).concat(or) : e;
}
var Si = /* @__PURE__ */ function(e) {
  ft(n, e);
  var t = dt(n);
  function n(o, r) {
    var i;
    _e(this, n), i = t.call(this), w(ge(i), "result", ""), w(ge(i), "unitlessCssVar", void 0), w(ge(i), "lowPriority", void 0);
    var s = V(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = xt(o) : s === "string" && (i.result = o), i;
  }
  return Te(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(xt(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(xt(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " * ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " * ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " / ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " / ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(r) {
      return this.lowPriority || r ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(r) {
      var i = this, s = r || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return i.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(bi, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(rr), xi = /* @__PURE__ */ function(e) {
  ft(n, e);
  var t = dt(n);
  function n(o) {
    var r;
    return _e(this, n), r = t.call(this), w(ge(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Te(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result += r.result : typeof r == "number" && (this.result += r), this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result -= r.result : typeof r == "number" && (this.result -= r), this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return r instanceof n ? this.result *= r.result : typeof r == "number" && (this.result *= r), this;
    }
  }, {
    key: "div",
    value: function(r) {
      return r instanceof n ? this.result /= r.result : typeof r == "number" && (this.result /= r), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(rr), Ci = function(t, n) {
  var o = t === "css" ? Si : xi;
  return function(r) {
    return new o(r, n);
  };
}, pn = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function gn(e, t, n, o) {
  var r = E({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var c = W(a, 2), l = c[0], f = c[1];
      if (r != null && r[l] || r != null && r[f]) {
        var u;
        (u = r[f]) !== null && u !== void 0 || (r[f] = r == null ? void 0 : r[l]);
      }
    });
  }
  var s = E(E({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var ir = typeof CSSINJS_STATISTIC < "u", Dt = !0;
function Ft() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!ir)
    return Object.assign.apply(Object, [{}].concat(t));
  Dt = !1;
  var o = {};
  return t.forEach(function(r) {
    if (V(r) === "object") {
      var i = Object.keys(r);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[s];
          }
        });
      });
    }
  }), Dt = !0, o;
}
var vn = {};
function Ei() {
}
var wi = function(t) {
  var n, o = t, r = Ei;
  return ir && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (Dt) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var c;
    vn[s] = {
      global: Array.from(n),
      component: E(E({}, (c = vn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function yn(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Ft(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function _i(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return Rt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return Rt(i);
      }).join(","), ")");
    }
  };
}
var Ti = 1e3 * 60 * 10, Ri = /* @__PURE__ */ function() {
  function e() {
    _e(this, e), w(this, "map", /* @__PURE__ */ new Map()), w(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), w(this, "nextID", 0), w(this, "lastAccessBeat", /* @__PURE__ */ new Map()), w(this, "accessBeat", 0);
  }
  return Te(e, [{
    key: "set",
    value: function(n, o) {
      this.clear();
      var r = this.getCompositeKey(n);
      this.map.set(r, o), this.lastAccessBeat.set(r, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var o = this.getCompositeKey(n), r = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, r;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var o = this, r = n.map(function(i) {
        return i && V(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(V(i), "_").concat(i);
      });
      return r.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var o = this.nextID;
      return this.objectIDMap.set(n, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(r, i) {
          o - r > Ti && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), bn = new Ri();
function Pi(e, t) {
  return y.useMemo(function() {
    var n = bn.get(t);
    if (n)
      return n;
    var o = e();
    return bn.set(t, o), o;
  }, t);
}
var Mi = function() {
  return {};
};
function Oi(e) {
  var t = e.useCSP, n = t === void 0 ? Mi : t, o = e.useToken, r = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, h, v, g) {
    var m = Array.isArray(d) ? d[0] : d;
    function x(P) {
      return "".concat(String(m)).concat(P.slice(0, 1).toUpperCase()).concat(P.slice(1));
    }
    var C = (g == null ? void 0 : g.unitless) || {}, _ = typeof a == "function" ? a(d) : {}, b = E(E({}, _), {}, w({}, x("zIndexPopup"), !0));
    Object.keys(C).forEach(function(P) {
      b[x(P)] = C[P];
    });
    var R = E(E({}, g), {}, {
      unitless: b,
      prefixToken: x
    }), S = f(d, h, v, R), T = l(m, v, R);
    return function(P) {
      var k = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : P, $ = S(P, k), D = W($, 2), A = D[1], L = T(k), j = W(L, 2), M = j[0], F = j[1];
      return [M, A, F];
    };
  }
  function l(d, h, v) {
    var g = v.unitless, m = v.injectStyle, x = m === void 0 ? !0 : m, C = v.prefixToken, _ = v.ignore, b = function(T) {
      var P = T.rootCls, k = T.cssVar, $ = k === void 0 ? {} : k, D = o(), A = D.realToken;
      return jr({
        path: [d],
        prefix: $.prefix,
        key: $.key,
        unitless: g,
        ignore: _,
        token: A,
        scope: P
      }, function() {
        var L = yn(d, A, h), j = gn(d, A, L, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(L).forEach(function(M) {
          j[C(M)] = j[M], delete j[M];
        }), j;
      }), null;
    }, R = function(T) {
      var P = o(), k = P.cssVar;
      return [function($) {
        return x && k ? /* @__PURE__ */ y.createElement(y.Fragment, null, /* @__PURE__ */ y.createElement(b, {
          rootCls: T,
          cssVar: k,
          component: d
        }), $) : $;
      }, k == null ? void 0 : k.key];
    };
    return R;
  }
  function f(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], x = W(m, 1), C = x[0], _ = m.join("-"), b = e.layer || {
      name: "antd"
    };
    return function(R) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : R, T = o(), P = T.theme, k = T.realToken, $ = T.hashId, D = T.token, A = T.cssVar, L = r(), j = L.rootPrefixCls, M = L.iconPrefixCls, F = n(), Q = A ? "css" : "js", N = Pi(function() {
        var G = /* @__PURE__ */ new Set();
        return A && Object.keys(g.unitless || {}).forEach(function(ne) {
          G.add(pt(ne, A.prefix)), G.add(pt(ne, pn(C, A.prefix)));
        }), Ci(Q, G);
      }, [Q, C, A == null ? void 0 : A.prefix]), fe = _i(Q), ye = fe.max, K = fe.min, oe = {
        theme: P,
        token: D,
        hashId: $,
        nonce: function() {
          return F.nonce;
        },
        clientOnly: g.clientOnly,
        layer: b,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof i == "function" && Xt(E(E({}, oe), {}, {
        clientOnly: !1,
        path: ["Shared", j]
      }), function() {
        return i(D, {
          prefix: {
            rootPrefixCls: j,
            iconPrefixCls: M
          },
          csp: F
        });
      });
      var de = Xt(E(E({}, oe), {}, {
        path: [_, R, M]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var G = wi(D), ne = G.token, Z = G.flush, J = yn(C, k, v), he = ".".concat(R), be = gn(C, k, J, {
          deprecatedTokens: g.deprecatedTokens
        });
        A && J && V(J) === "object" && Object.keys(J).forEach(function(Re) {
          J[Re] = "var(".concat(pt(Re, pn(C, A.prefix)), ")");
        });
        var me = Ft(ne, {
          componentCls: he,
          prefixCls: R,
          iconCls: ".".concat(M),
          antCls: ".".concat(j),
          calc: N,
          // @ts-ignore
          max: ye,
          // @ts-ignore
          min: K
        }, A ? J : be), Se = h(me, {
          hashId: $,
          prefixCls: R,
          rootPrefixCls: j,
          iconPrefixCls: M
        });
        Z(C, be);
        var ie = typeof s == "function" ? s(me, R, S, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : ie, Se];
      });
      return [de, $];
    };
  }
  function u(d, h, v) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = f(d, h, v, E({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), x = function(_) {
      var b = _.prefixCls, R = _.rootCls, S = R === void 0 ? b : R;
      return m(b, S), null;
    };
    return x;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
const H = Math.round;
function Ct(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const Sn = (e, t, n) => n === 0 ? e : e / 100;
function Le(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class ce {
  constructor(t) {
    w(this, "isValid", !0), w(this, "r", 0), w(this, "g", 0), w(this, "b", 0), w(this, "a", 1), w(this, "_h", void 0), w(this, "_s", void 0), w(this, "_l", void 0), w(this, "_v", void 0), w(this, "_max", void 0), w(this, "_min", void 0), w(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof ce)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Le(t.r), this.g = Le(t.g), this.b = Le(t.b), this.a = typeof t.a == "number" ? Le(t.a, 1) : 1;
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
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = H(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - t / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + t / 100;
    return r > 1 && (r = 1), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const o = this._c(t), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
      r: H(i("r")),
      g: H(i("g")),
      b: H(i("b")),
      a: H(i("a") * 100) / 100
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
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (i) => H((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
    return this._c({
      r: r("r"),
      g: r("g"),
      b: r("b"),
      a: o
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
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (t += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = H(this.a * 255).toString(16);
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
    const t = this.getHue(), n = H(this.getSaturation() * 100), o = H(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${o}%,${this.a})` : `hsl(${t},${n}%,${o}%)`;
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
  _sc(t, n, o) {
    const r = this.clone();
    return r[t] = Le(n, o), r;
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
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = t % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = H(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, l = (1 - Math.abs(2 * o - 1)) * n, f = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = l, s = f) : c >= 1 && c < 2 ? (i = f, s = l) : c >= 2 && c < 3 ? (s = l, a = f) : c >= 3 && c < 4 ? (s = f, a = l) : c >= 4 && c < 5 ? (i = f, a = l) : c >= 5 && c < 6 && (i = l, a = f);
    const u = o - l / 2;
    this.r = H((i + u) * 255), this.g = H((s + u) * 255), this.b = H((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = H(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, l = H(o * (1 - n) * 255), f = H(o * (1 - n * c) * 255), u = H(o * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = l;
        break;
      case 1:
        this.r = f, this.b = l;
        break;
      case 2:
        this.r = l, this.b = u;
        break;
      case 3:
        this.r = l, this.g = f;
        break;
      case 4:
        this.r = u, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = Ct(t, Sn);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Ct(t, Sn);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Ct(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? H(o / 100 * 255) : o
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
}, ki = Object.assign(Object.assign({}, Ai), {
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
function ze(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new ce(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new ce(t).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const f = Math.round((n - s * (1 - l)) / l), u = Math.round((o - a * (1 - l)) / l), d = Math.round((r - c * (1 - l)) / l);
    if (Et(f) && Et(u) && Et(d))
      return new ce({
        r: f,
        g: u,
        b: d,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new ce({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var Li = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function Ii(e) {
  const {
    override: t
  } = e, n = Li(e, ["override"]), o = Object.assign({}, t);
  Object.keys(ki).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, c = 992, l = 1200, f = 1600;
  if (r.motion === !1) {
    const d = "0s";
    r.motionDurationFast = d, r.motionDurationMid = d, r.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: ze(r.colorBorderSecondary, r.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: r.colorTextQuaternary,
    colorTextDisabled: r.colorTextQuaternary,
    colorTextHeading: r.colorText,
    colorTextLabel: r.colorTextSecondary,
    colorTextDescription: r.colorTextTertiary,
    colorTextLightSolid: r.colorWhite,
    colorHighlight: r.colorError,
    colorBgTextHover: r.colorFillSecondary,
    colorBgTextActive: r.colorFill,
    colorIcon: r.colorTextTertiary,
    colorIconHover: r.colorText,
    colorErrorOutline: ze(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: ze(r.colorWarningBg, r.colorBgContainer),
    // Font
    fontSizeIcon: r.fontSizeSM,
    // Line
    lineWidthFocus: r.lineWidth * 3,
    // Control
    lineWidth: r.lineWidth,
    controlOutlineWidth: r.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: r.controlHeight / 2,
    controlItemBgHover: r.colorFillTertiary,
    controlItemBgActive: r.colorPrimaryBg,
    controlItemBgActiveHover: r.colorPrimaryBgHover,
    controlItemBgActiveDisabled: r.colorFill,
    controlTmpOutline: r.colorFillQuaternary,
    controlOutline: ze(r.colorPrimaryBg, r.colorBgContainer),
    lineType: r.lineType,
    borderRadius: r.borderRadius,
    borderRadiusXS: r.borderRadiusXS,
    borderRadiusSM: r.borderRadiusSM,
    borderRadiusLG: r.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: r.sizeXXS,
    paddingXS: r.sizeXS,
    paddingSM: r.sizeSM,
    padding: r.size,
    paddingMD: r.sizeMD,
    paddingLG: r.sizeLG,
    paddingXL: r.sizeXL,
    paddingContentHorizontalLG: r.sizeLG,
    paddingContentVerticalLG: r.sizeMS,
    paddingContentHorizontal: r.sizeMS,
    paddingContentVertical: r.sizeSM,
    paddingContentHorizontalSM: r.size,
    paddingContentVerticalSM: r.sizeXS,
    marginXXS: r.sizeXXS,
    marginXS: r.sizeXS,
    marginSM: r.sizeSM,
    margin: r.size,
    marginMD: r.sizeMD,
    marginLG: r.sizeLG,
    marginXL: r.sizeXL,
    marginXXL: r.sizeXXL,
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
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ce("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ce("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ce("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), o);
}
const ji = {
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
}, $i = {
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
}, Di = $r(Tt.defaultAlgorithm), Ni = {
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
}, sr = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...i
  } = t;
  let s = {
    ...o,
    override: r
  };
  return s = Ii(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: l,
      ...f
    } = c;
    let u = f;
    l && (u = sr({
      ...s,
      ...f
    }, {
      override: f
    }, l)), s[a] = u;
  }), s;
};
function Bi() {
  const {
    token: e,
    hashed: t,
    theme: n = Di,
    override: o,
    cssVar: r
  } = y.useContext(Tt._internalContext), [i, s, a] = Dr(n, [Tt.defaultSeed, e], {
    salt: `${Po}-${t || ""}`,
    override: o,
    getComputedToken: sr,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: ji,
      ignore: $i,
      preserve: Ni
    }
  });
  return [n, a, t ? s : "", i, r];
}
const {
  genStyleHooks: Hi
} = Oi({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Ot();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = Bi();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Ot();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var Vi = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, Fi = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, zi = "".concat(Vi, " ").concat(Fi).split(/[\s\n]+/), Xi = "aria-", Ui = "data-";
function xn(e, t) {
  return e.indexOf(t) === 0;
}
function Wi(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = E({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || xn(r, Xi)) || // Data
    n.data && xn(r, Ui) || // Attr
    n.attr && zi.includes(r)) && (o[r] = e[r]);
  }), o;
}
function Ki(e, t) {
  return gr(e, () => {
    const n = t(), {
      nativeElement: o
    } = n;
    return new Proxy(o, {
      get(r, i) {
        return n[i] ? n[i] : Reflect.get(r, i);
      }
    });
  });
}
const ar = /* @__PURE__ */ p.createContext({}), Cn = () => ({
  height: 0
}), En = (e) => ({
  height: e.scrollHeight
});
function Gi(e) {
  const {
    title: t,
    onOpenChange: n,
    open: o,
    children: r,
    className: i,
    style: s,
    classNames: a = {},
    styles: c = {},
    closable: l,
    forceRender: f
  } = e, {
    prefixCls: u
  } = p.useContext(ar), d = `${u}-header`;
  return /* @__PURE__ */ p.createElement(nr, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${d}-motion`,
    leavedClassName: `${d}-motion-hidden`,
    onEnterStart: Cn,
    onEnterActive: En,
    onLeaveStart: En,
    onLeaveActive: Cn,
    visible: o,
    forceRender: f
  }, ({
    className: h,
    style: v
  }) => /* @__PURE__ */ p.createElement("div", {
    className: te(d, h, i),
    style: {
      ...v,
      ...s
    }
  }, (l !== !1 || t) && /* @__PURE__ */ p.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      te(`${d}-header`, a.header)
    ),
    style: {
      ...c.header
    }
  }, /* @__PURE__ */ p.createElement("div", {
    className: `${d}-title`
  }, t), l !== !1 && /* @__PURE__ */ p.createElement("div", {
    className: `${d}-close`
  }, /* @__PURE__ */ p.createElement(An, {
    type: "text",
    icon: /* @__PURE__ */ p.createElement(Or, null),
    size: "small",
    onClick: () => {
      n == null || n(!o);
    }
  }))), r && /* @__PURE__ */ p.createElement("div", {
    className: te(`${d}-content`, a.content),
    style: {
      ...c.content
    }
  }, r)));
}
const ht = /* @__PURE__ */ p.createContext(null);
function qi(e, t) {
  const {
    className: n,
    action: o,
    onClick: r,
    ...i
  } = e, s = p.useContext(ht), {
    prefixCls: a,
    disabled: c
  } = s, l = s[o], f = c ?? i.disabled ?? s[`${o}Disabled`];
  return /* @__PURE__ */ p.createElement(An, le({
    type: "text"
  }, i, {
    ref: t,
    onClick: (u) => {
      f || (l && l(), r && r(u));
    },
    className: te(a, n, {
      [`${a}-disabled`]: f
    })
  }));
}
const mt = /* @__PURE__ */ p.forwardRef(qi);
function Qi(e, t) {
  return /* @__PURE__ */ p.createElement(mt, le({
    icon: /* @__PURE__ */ p.createElement(Ar, null)
  }, e, {
    action: "onClear",
    ref: t
  }));
}
const Yi = /* @__PURE__ */ p.forwardRef(Qi), Zi = /* @__PURE__ */ vr((e) => {
  const {
    className: t
  } = e;
  return /* @__PURE__ */ y.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    className: t
  }, /* @__PURE__ */ y.createElement("title", null, "Stop Loading"), /* @__PURE__ */ y.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ y.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ y.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ y.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function Ji(e, t) {
  const {
    prefixCls: n
  } = p.useContext(ht), {
    className: o
  } = e;
  return /* @__PURE__ */ p.createElement(mt, le({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, e, {
    className: te(o, `${n}-loading-button`),
    action: "onCancel",
    ref: t
  }), /* @__PURE__ */ p.createElement(Zi, {
    className: `${n}-loading-icon`
  }));
}
const cr = /* @__PURE__ */ p.forwardRef(Ji);
function es(e, t) {
  return /* @__PURE__ */ p.createElement(mt, le({
    icon: /* @__PURE__ */ p.createElement(kr, null),
    type: "primary",
    shape: "circle"
  }, e, {
    action: "onSend",
    ref: t
  }));
}
const lr = /* @__PURE__ */ p.forwardRef(es), Ie = 1e3, je = 4, qe = 140, wn = qe / 2, Xe = 250, _n = 500, Ue = 0.8;
function ts({
  className: e
}) {
  return /* @__PURE__ */ y.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${Ie} ${Ie}`,
    xmlns: "http://www.w3.org/2000/svg",
    className: e
  }, /* @__PURE__ */ y.createElement("title", null, "Speech Recording"), Array.from({
    length: je
  }).map((t, n) => {
    const o = (Ie - qe * je) / (je - 1), r = n * (o + qe), i = Ie / 2 - Xe / 2, s = Ie / 2 - _n / 2;
    return /* @__PURE__ */ y.createElement("rect", {
      fill: "currentColor",
      rx: wn,
      ry: wn,
      height: Xe,
      width: qe,
      x: r,
      y: i,
      key: n
    }, /* @__PURE__ */ y.createElement("animate", {
      attributeName: "height",
      values: `${Xe}; ${_n}; ${Xe}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Ue}s`,
      begin: `${Ue / je * n}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ y.createElement("animate", {
      attributeName: "y",
      values: `${i}; ${s}; ${i}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Ue}s`,
      begin: `${Ue / je * n}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function ns(e, t) {
  const {
    speechRecording: n,
    onSpeechDisabled: o,
    prefixCls: r
  } = p.useContext(ht);
  let i = null;
  return n ? i = /* @__PURE__ */ p.createElement(ts, {
    className: `${r}-recording-icon`
  }) : o ? i = /* @__PURE__ */ p.createElement(Lr, null) : i = /* @__PURE__ */ p.createElement(Ir, null), /* @__PURE__ */ p.createElement(mt, le({
    icon: i,
    color: "primary",
    variant: "text"
  }, e, {
    action: "onSpeech",
    ref: t
  }));
}
const ur = /* @__PURE__ */ p.forwardRef(ns), rs = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, o = `${t}-header`;
  return {
    [t]: {
      [o]: {
        borderBottomWidth: e.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: e.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: e.colorFillAlter,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          paddingBlock: n(e.paddingSM).sub(e.lineWidthBold).equal(),
          paddingInlineStart: e.padding,
          paddingInlineEnd: e.paddingXS,
          display: "flex",
          [`${o}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: e.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((r) => `${r} ${e.motionDurationSlow}`).join(","),
          overflow: "hidden",
          "&-enter-start, &-leave-active": {
            borderBottomColor: "transparent"
          },
          "&-hidden": {
            display: "none"
          }
        }
      }
    }
  };
}, os = (e) => {
  const {
    componentCls: t,
    padding: n,
    paddingSM: o,
    paddingXS: r,
    paddingXXS: i,
    lineWidth: s,
    lineWidthBold: a,
    calc: c
  } = e;
  return {
    [t]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${e.boxShadowTertiary}`,
      transition: `background ${e.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: c(e.borderRadius).mul(2).equal()
      },
      borderColor: e.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${e.motionDurationSlow}`,
        borderRadius: {
          _skip_check_: !0,
          value: "inherit"
        },
        borderStyle: "inherit",
        borderColor: "inherit",
        borderWidth: s
      },
      // Focus
      "&:focus-within": {
        boxShadow: `${e.boxShadowSecondary}`,
        borderColor: e.colorPrimary,
        "&:after": {
          borderWidth: a
        }
      },
      "&-disabled": {
        background: e.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${t}-content`]: {
        display: "flex",
        gap: r,
        width: "100%",
        paddingBlock: o,
        paddingInlineStart: n,
        paddingInlineEnd: o,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${t}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${t}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${t}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: e.paddingXS
        }
      },
      [`${t}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: e.controlHeight,
          width: e.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      },
      // ============================ Footer =============================
      [`${t}-footer`]: {
        paddingInlineStart: n,
        paddingInlineEnd: o,
        paddingBlockEnd: o,
        paddingBlockStart: i,
        boxSizing: "border-box"
      }
    }
  };
}, is = () => ({}), ss = Hi("Sender", (e) => {
  const {
    paddingXS: t,
    calc: n
  } = e, o = Ft(e, {
    SenderContentMaxWidth: `calc(100% - ${Rt(n(t).add(32).equal())})`
  });
  return [os(o), rs(o)];
}, is);
let Ze;
!Ze && typeof window < "u" && (Ze = window.SpeechRecognition || window.webkitSpeechRecognition);
function as(e, t) {
  const n = ve(e), [o, r, i] = y.useMemo(() => typeof t == "object" ? [t.recording, t.onRecordingChange, typeof t.recording == "boolean"] : [void 0, void 0, !1], [t]), [s, a] = y.useState(null);
  y.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let g = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((m) => {
        a(m.state), m.onchange = function() {
          a(this.state);
        }, g = m;
      }), () => {
        g && (g.onchange = null);
      };
    }
  }, []);
  const c = Ze && s !== "denied", l = y.useRef(null), [f, u] = Nn(!1, {
    value: o
  }), d = y.useRef(!1), h = () => {
    if (c && !l.current) {
      const g = new Ze();
      g.onstart = () => {
        u(!0);
      }, g.onend = () => {
        u(!1);
      }, g.onresult = (m) => {
        var x, C, _;
        if (!d.current) {
          const b = (_ = (C = (x = m.results) == null ? void 0 : x[0]) == null ? void 0 : C[0]) == null ? void 0 : _.transcript;
          n(b);
        }
        d.current = !1;
      }, l.current = g;
    }
  }, v = ve((g) => {
    g && !f || (d.current = g, i ? r == null || r(!f) : (h(), l.current && (f ? (l.current.stop(), r == null || r(!1)) : (l.current.start(), r == null || r(!0)))));
  });
  return [c, v, f];
}
function cs(e, t, n) {
  return Ko(e, t) || n;
}
const Tn = {
  SendButton: lr,
  ClearButton: Yi,
  LoadingButton: cr,
  SpeechButton: ur
}, ls = /* @__PURE__ */ y.forwardRef((e, t) => {
  const {
    prefixCls: n,
    styles: o = {},
    classNames: r = {},
    className: i,
    rootClassName: s,
    style: a,
    defaultValue: c,
    value: l,
    readOnly: f,
    submitType: u = "enter",
    onSubmit: d,
    loading: h,
    components: v,
    onCancel: g,
    onChange: m,
    actions: x,
    onKeyPress: C,
    onKeyDown: _,
    disabled: b,
    allowSpeech: R,
    prefix: S,
    footer: T,
    header: P,
    onPaste: k,
    onPasteFile: $,
    autoSize: D = {
      maxRows: 8
    },
    ...A
  } = e, {
    direction: L,
    getPrefixCls: j
  } = Ot(), M = j("sender", n), F = y.useRef(null), Q = y.useRef(null);
  Ki(t, () => {
    var I, U;
    return {
      nativeElement: F.current,
      focus: (I = Q.current) == null ? void 0 : I.focus,
      blur: (U = Q.current) == null ? void 0 : U.blur
    };
  });
  const N = Ao("sender"), fe = `${M}-input`, [ye, K, oe] = ss(M), de = te(M, N.className, i, s, K, oe, {
    [`${M}-rtl`]: L === "rtl",
    [`${M}-disabled`]: b
  }), G = `${M}-actions-btn`, ne = `${M}-actions-list`, [Z, J] = Nn(c || "", {
    value: l
  }), he = (I, U) => {
    J(I), m && m(I, U);
  }, [be, me, Se] = as((I) => {
    he(`${Z} ${I}`);
  }, R), ie = cs(v, ["input"], Pr.TextArea), De = {
    ...Wi(A, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: Q
  }, Pe = () => {
    Z && d && !h && d(Z);
  }, se = () => {
    he("");
  }, Me = y.useRef(!1), Ne = () => {
    Me.current = !0;
  }, Oe = () => {
    Me.current = !1;
  }, Ae = (I) => {
    const U = I.key === "Enter" && !Me.current;
    switch (u) {
      case "enter":
        U && !I.shiftKey && (I.preventDefault(), Pe());
        break;
      case "shiftEnter":
        U && I.shiftKey && (I.preventDefault(), Pe());
        break;
    }
    C && C(I);
  }, z = (I) => {
    var ke;
    const U = (ke = I.clipboardData) == null ? void 0 : ke.files;
    U != null && U.length && $ && ($(U[0], U), I.preventDefault()), k == null || k(I);
  }, B = (I) => {
    var U, ke;
    I.target !== ((U = F.current) == null ? void 0 : U.querySelector(`.${fe}`)) && I.preventDefault(), (ke = Q.current) == null || ke.focus();
  };
  let X = /* @__PURE__ */ y.createElement(Mr, {
    className: `${ne}-presets`
  }, R && /* @__PURE__ */ y.createElement(ur, null), h ? /* @__PURE__ */ y.createElement(cr, null) : /* @__PURE__ */ y.createElement(lr, null));
  typeof x == "function" ? X = x(X, {
    components: Tn
  }) : (x || x === !1) && (X = x);
  const xe = {
    prefixCls: G,
    onSend: Pe,
    onSendDisabled: !Z,
    onClear: se,
    onClearDisabled: !Z,
    onCancel: g,
    onCancelDisabled: !h,
    onSpeech: () => me(!1),
    onSpeechDisabled: !be,
    speechRecording: Se,
    disabled: b
  };
  let ae = null;
  return typeof T == "function" ? ae = T({
    components: Tn
  }) : T && (ae = T), ye(/* @__PURE__ */ y.createElement("div", {
    ref: F,
    className: de,
    style: {
      ...N.style,
      ...a
    }
  }, P && /* @__PURE__ */ y.createElement(ar.Provider, {
    value: {
      prefixCls: M
    }
  }, P), /* @__PURE__ */ y.createElement(ht.Provider, {
    value: xe
  }, /* @__PURE__ */ y.createElement("div", {
    className: `${M}-content`,
    onMouseDown: B
  }, S && /* @__PURE__ */ y.createElement("div", {
    className: te(`${M}-prefix`, N.classNames.prefix, r.prefix),
    style: {
      ...N.styles.prefix,
      ...o.prefix
    }
  }, S), /* @__PURE__ */ y.createElement(ie, le({}, De, {
    disabled: b,
    style: {
      ...N.styles.input,
      ...o.input
    },
    className: te(fe, N.classNames.input, r.input),
    autoSize: D,
    value: Z,
    onChange: (I) => {
      he(I.target.value, I), me(!0);
    },
    onPressEnter: Ae,
    onCompositionStart: Ne,
    onCompositionEnd: Oe,
    onKeyDown: _,
    onPaste: z,
    variant: "borderless",
    readOnly: f
  })), X && /* @__PURE__ */ y.createElement("div", {
    className: te(ne, N.classNames.actions, r.actions),
    style: {
      ...N.styles.actions,
      ...o.actions
    }
  }, X)), ae && /* @__PURE__ */ y.createElement("div", {
    className: te(`${M}-footer`, N.classNames.footer, r.footer),
    style: {
      ...N.styles.footer,
      ...o.footer
    }
  }, ae))));
}), fr = ls;
fr.Header = Gi;
function us(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function fs(e, t = !1) {
  try {
    if (Er(e))
      return e;
    if (t && !us(e))
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
function Rn(e, t) {
  return yr(() => fs(e, t), [e, t]);
}
function ds({
  value: e,
  onValueChange: t
}) {
  const [n, o] = On(e), r = re(t);
  r.current = t;
  const i = re(n);
  return i.current = n, pe(() => {
    r.current(n);
  }, [n]), pe(() => {
    Qr(e, i.current) || o(e);
  }, [e]), [n, o];
}
const hs = ({
  children: e,
  ...t
}) => /* @__PURE__ */ q.jsx(q.Fragment, {
  children: e(t)
});
function ms(e) {
  return y.createElement(hs, {
    children: e
  });
}
function Pn(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ms((n) => /* @__PURE__ */ q.jsx(_r, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ q.jsx(Qe, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ q.jsx(Qe, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Mn({
  key: e,
  slots: t,
  targets: n
}, o) {
  return t[e] ? (...r) => n ? n.map((i, s) => /* @__PURE__ */ q.jsx(y.Fragment, {
    children: Pn(i, {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }, s)) : /* @__PURE__ */ q.jsx(q.Fragment, {
    children: Pn(t[e], {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }) : void 0;
}
const vs = Eo(({
  slots: e,
  children: t,
  setSlotParams: n,
  onValueChange: o,
  onChange: r,
  onPasteFile: i,
  upload: s,
  elRef: a,
  ...c
}) => {
  const l = Rn(c.actions, !0), f = Rn(c.footer, !0), [u, d] = ds({
    onValueChange: o,
    value: c.value
  }), h = Tr();
  return /* @__PURE__ */ q.jsxs(q.Fragment, {
    children: [/* @__PURE__ */ q.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ q.jsx(fr, {
      ...c,
      value: u,
      ref: a,
      onSubmit: (...v) => {
        var g;
        h || (g = c.onSubmit) == null || g.call(c, ...v);
      },
      onChange: (v) => {
        r == null || r(v), d(v);
      },
      onPasteFile: async (v, g) => {
        const m = await s(Array.from(g));
        i == null || i(m.map((x) => x.path));
      },
      header: e.header ? /* @__PURE__ */ q.jsx(Qe, {
        slot: e.header
      }) : c.header,
      prefix: e.prefix ? /* @__PURE__ */ q.jsx(Qe, {
        slot: e.prefix
      }) : c.prefix,
      actions: e.actions ? Mn({
        slots: e,
        key: "actions"
      }, {}) : l || c.actions,
      footer: e.footer ? Mn({
        slots: e,
        key: "footer"
      }) : f || c.footer
    })]
  });
});
export {
  vs as Sender,
  vs as default
};

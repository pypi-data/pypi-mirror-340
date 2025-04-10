import { i as ei, a as Ut, r as ti, b as ni, w as it, g as ri, c as J, d as ii, e as oi, o as si } from "./Index-B4A8WRBt.js";
const R = window.ms_globals.React, f = window.ms_globals.React, Gr = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, He = window.ms_globals.React.useState, Se = window.ms_globals.React.useEffect, qr = window.ms_globals.React.version, Kr = window.ms_globals.React.isValidElement, Yr = window.ms_globals.React.useLayoutEffect, Zr = window.ms_globals.React.useImperativeHandle, Qr = window.ms_globals.React.memo, Vt = window.ms_globals.React.useMemo, Jr = window.ms_globals.React.useCallback, hn = window.ms_globals.ReactDOM, ut = window.ms_globals.ReactDOM.createPortal, ai = window.ms_globals.internalContext.useContextPropsContext, li = window.ms_globals.internalContext.ContextPropsProvider, ci = window.ms_globals.internalContext.useSuggestionOpenContext, ui = window.ms_globals.antdIcons.FileTextFilled, di = window.ms_globals.antdIcons.CloseCircleFilled, fi = window.ms_globals.antdIcons.FileExcelFilled, hi = window.ms_globals.antdIcons.FileImageFilled, pi = window.ms_globals.antdIcons.FileMarkdownFilled, mi = window.ms_globals.antdIcons.FilePdfFilled, gi = window.ms_globals.antdIcons.FilePptFilled, vi = window.ms_globals.antdIcons.FileWordFilled, bi = window.ms_globals.antdIcons.FileZipFilled, yi = window.ms_globals.antdIcons.PlusOutlined, wi = window.ms_globals.antdIcons.LeftOutlined, Si = window.ms_globals.antdIcons.RightOutlined, xi = window.ms_globals.antdIcons.CloseOutlined, Ci = window.ms_globals.antdIcons.ClearOutlined, Ei = window.ms_globals.antdIcons.ArrowUpOutlined, _i = window.ms_globals.antdIcons.AudioMutedOutlined, Ri = window.ms_globals.antdIcons.AudioOutlined, Ti = window.ms_globals.antdIcons.CloudUploadOutlined, Pi = window.ms_globals.antdIcons.LinkOutlined, Mi = window.ms_globals.antd.ConfigProvider, ir = window.ms_globals.antd.Upload, ze = window.ms_globals.antd.theme, Li = window.ms_globals.antd.Progress, Oi = window.ms_globals.antd.Image, Ae = window.ms_globals.antd.Button, or = window.ms_globals.antd.Flex, Lt = window.ms_globals.antd.Typography, Ai = window.ms_globals.antd.Input, $i = window.ms_globals.antd.Tooltip, Ii = window.ms_globals.antd.Badge, Xt = window.ms_globals.antdCssinjs.unit, Ot = window.ms_globals.antdCssinjs.token2CSSVar, pn = window.ms_globals.antdCssinjs.useStyleRegister, ki = window.ms_globals.antdCssinjs.useCSSVarRegister, Di = window.ms_globals.antdCssinjs.createTheme, Ni = window.ms_globals.antdCssinjs.useCacheToken;
var Fi = /\s/;
function Wi(n) {
  for (var e = n.length; e-- && Fi.test(n.charAt(e)); )
    ;
  return e;
}
var ji = /^\s+/;
function Bi(n) {
  return n && n.slice(0, Wi(n) + 1).replace(ji, "");
}
var mn = NaN, Hi = /^[-+]0x[0-9a-f]+$/i, zi = /^0b[01]+$/i, Vi = /^0o[0-7]+$/i, Ui = parseInt;
function gn(n) {
  if (typeof n == "number")
    return n;
  if (ei(n))
    return mn;
  if (Ut(n)) {
    var e = typeof n.valueOf == "function" ? n.valueOf() : n;
    n = Ut(e) ? e + "" : e;
  }
  if (typeof n != "string")
    return n === 0 ? n : +n;
  n = Bi(n);
  var t = zi.test(n);
  return t || Vi.test(n) ? Ui(n.slice(2), t ? 2 : 8) : Hi.test(n) ? mn : +n;
}
function Xi() {
}
var At = function() {
  return ti.Date.now();
}, Gi = "Expected a function", qi = Math.max, Ki = Math.min;
function Yi(n, e, t) {
  var r, i, o, s, a, c, l = 0, u = !1, d = !1, h = !0;
  if (typeof n != "function")
    throw new TypeError(Gi);
  e = gn(e) || 0, Ut(t) && (u = !!t.leading, d = "maxWait" in t, o = d ? qi(gn(t.maxWait) || 0, e) : o, h = "trailing" in t ? !!t.trailing : h);
  function p(S) {
    var T = r, E = i;
    return r = i = void 0, l = S, s = n.apply(E, T), s;
  }
  function b(S) {
    return l = S, a = setTimeout(m, e), u ? p(S) : s;
  }
  function v(S) {
    var T = S - c, E = S - l, P = e - T;
    return d ? Ki(P, o - E) : P;
  }
  function g(S) {
    var T = S - c, E = S - l;
    return c === void 0 || T >= e || T < 0 || d && E >= o;
  }
  function m() {
    var S = At();
    if (g(S))
      return x(S);
    a = setTimeout(m, v(S));
  }
  function x(S) {
    return a = void 0, h && r ? p(S) : (r = i = void 0, s);
  }
  function _() {
    a !== void 0 && clearTimeout(a), l = 0, r = c = i = a = void 0;
  }
  function y() {
    return a === void 0 ? s : x(At());
  }
  function C() {
    var S = At(), T = g(S);
    if (r = arguments, i = this, c = S, T) {
      if (a === void 0)
        return b(c);
      if (d)
        return clearTimeout(a), a = setTimeout(m, e), p(c);
    }
    return a === void 0 && (a = setTimeout(m, e)), s;
  }
  return C.cancel = _, C.flush = y, C;
}
function Zi(n, e) {
  return ni(n, e);
}
var sr = {
  exports: {}
}, ht = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Qi = f, Ji = Symbol.for("react.element"), eo = Symbol.for("react.fragment"), to = Object.prototype.hasOwnProperty, no = Qi.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ro = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ar(n, e, t) {
  var r, i = {}, o = null, s = null;
  t !== void 0 && (o = "" + t), e.key !== void 0 && (o = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) to.call(e, r) && !ro.hasOwnProperty(r) && (i[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) i[r] === void 0 && (i[r] = e[r]);
  return {
    $$typeof: Ji,
    type: n,
    key: o,
    ref: s,
    props: i,
    _owner: no.current
  };
}
ht.Fragment = eo;
ht.jsx = ar;
ht.jsxs = ar;
sr.exports = ht;
var Y = sr.exports;
const {
  SvelteComponent: io,
  assign: vn,
  binding_callbacks: bn,
  check_outros: oo,
  children: lr,
  claim_element: cr,
  claim_space: so,
  component_subscribe: yn,
  compute_slots: ao,
  create_slot: lo,
  detach: Me,
  element: ur,
  empty: wn,
  exclude_internal_props: Sn,
  get_all_dirty_from_scope: co,
  get_slot_changes: uo,
  group_outros: fo,
  init: ho,
  insert_hydration: ot,
  safe_not_equal: po,
  set_custom_element_data: dr,
  space: mo,
  transition_in: st,
  transition_out: Gt,
  update_slot_base: go
} = window.__gradio__svelte__internal, {
  beforeUpdate: vo,
  getContext: bo,
  onDestroy: yo,
  setContext: wo
} = window.__gradio__svelte__internal;
function xn(n) {
  let e, t;
  const r = (
    /*#slots*/
    n[7].default
  ), i = lo(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = ur("svelte-slot"), i && i.c(), this.h();
    },
    l(o) {
      e = cr(o, "SVELTE-SLOT", {
        class: !0
      });
      var s = lr(e);
      i && i.l(s), s.forEach(Me), this.h();
    },
    h() {
      dr(e, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      ot(o, e, s), i && i.m(e, null), n[9](e), t = !0;
    },
    p(o, s) {
      i && i.p && (!t || s & /*$$scope*/
      64) && go(
        i,
        r,
        o,
        /*$$scope*/
        o[6],
        t ? uo(
          r,
          /*$$scope*/
          o[6],
          s,
          null
        ) : co(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      t || (st(i, o), t = !0);
    },
    o(o) {
      Gt(i, o), t = !1;
    },
    d(o) {
      o && Me(e), i && i.d(o), n[9](null);
    }
  };
}
function So(n) {
  let e, t, r, i, o = (
    /*$$slots*/
    n[4].default && xn(n)
  );
  return {
    c() {
      e = ur("react-portal-target"), t = mo(), o && o.c(), r = wn(), this.h();
    },
    l(s) {
      e = cr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), lr(e).forEach(Me), t = so(s), o && o.l(s), r = wn(), this.h();
    },
    h() {
      dr(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      ot(s, e, a), n[8](e), ot(s, t, a), o && o.m(s, a), ot(s, r, a), i = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, a), a & /*$$slots*/
      16 && st(o, 1)) : (o = xn(s), o.c(), st(o, 1), o.m(r.parentNode, r)) : o && (fo(), Gt(o, 1, 1, () => {
        o = null;
      }), oo());
    },
    i(s) {
      i || (st(o), i = !0);
    },
    o(s) {
      Gt(o), i = !1;
    },
    d(s) {
      s && (Me(e), Me(t), Me(r)), n[8](null), o && o.d(s);
    }
  };
}
function Cn(n) {
  const {
    svelteInit: e,
    ...t
  } = n;
  return t;
}
function xo(n, e, t) {
  let r, i, {
    $$slots: o = {},
    $$scope: s
  } = e;
  const a = ao(o);
  let {
    svelteInit: c
  } = e;
  const l = it(Cn(e)), u = it();
  yn(n, u, (y) => t(0, r = y));
  const d = it();
  yn(n, d, (y) => t(1, i = y));
  const h = [], p = bo("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: v,
    subSlotIndex: g
  } = ri() || {}, m = c({
    parent: p,
    props: l,
    target: u,
    slot: d,
    slotKey: b,
    slotIndex: v,
    subSlotIndex: g,
    onDestroy(y) {
      h.push(y);
    }
  });
  wo("$$ms-gr-react-wrapper", m), vo(() => {
    l.set(Cn(e));
  }), yo(() => {
    h.forEach((y) => y());
  });
  function x(y) {
    bn[y ? "unshift" : "push"](() => {
      r = y, u.set(r);
    });
  }
  function _(y) {
    bn[y ? "unshift" : "push"](() => {
      i = y, d.set(i);
    });
  }
  return n.$$set = (y) => {
    t(17, e = vn(vn({}, e), Sn(y))), "svelteInit" in y && t(5, c = y.svelteInit), "$$scope" in y && t(6, s = y.$$scope);
  }, e = Sn(e), [r, i, u, d, a, c, s, o, x, _];
}
class Co extends io {
  constructor(e) {
    super(), ho(this, e, xo, So, po, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: nl
} = window.__gradio__svelte__internal, En = window.ms_globals.rerender, $t = window.ms_globals.tree;
function Eo(n, e = {}) {
  function t(r) {
    const i = it(), o = new Co({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: n,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? $t;
          return c.nodes = [...c.nodes, a], En({
            createPortal: ut,
            node: $t
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== i), En({
              createPortal: ut,
              node: $t
            });
          }), a;
        },
        ...r.props
      }
    });
    return i.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const _o = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ro(n) {
  return n ? Object.keys(n).reduce((e, t) => {
    const r = n[t];
    return e[t] = To(t, r), e;
  }, {}) : {};
}
function To(n, e) {
  return typeof e == "number" && !_o.includes(n) ? e + "px" : e;
}
function qt(n) {
  const e = [], t = n.cloneNode(!1);
  if (n._reactElement) {
    const i = f.Children.toArray(n._reactElement.props.children).map((o) => {
      if (f.isValidElement(o) && o.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = qt(o.props.el);
        return f.cloneElement(o, {
          ...o.props,
          el: a,
          children: [...f.Children.toArray(o.props.children), ...s]
        });
      }
      return null;
    });
    return i.originalChildren = n._reactElement.props.children, e.push(ut(f.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: i
    }), t)), {
      clonedElement: t,
      portals: e
    };
  }
  Object.keys(n.getEventListeners()).forEach((i) => {
    n.getEventListeners(i).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      t.addEventListener(a, s, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let i = 0; i < r.length; i++) {
    const o = r[i];
    if (o.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = qt(o);
      e.push(...a), t.appendChild(s);
    } else o.nodeType === 3 && t.appendChild(o.cloneNode());
  }
  return {
    clonedElement: t,
    portals: e
  };
}
function Po(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const Kt = Gr(({
  slot: n,
  clone: e,
  className: t,
  style: r,
  observeAttributes: i
}, o) => {
  const s = de(), [a, c] = He([]), {
    forceClone: l
  } = ai(), u = l ? !0 : e;
  return Se(() => {
    var v;
    if (!s.current || !n)
      return;
    let d = n;
    function h() {
      let g = d;
      if (d.tagName.toLowerCase() === "svelte-slot" && d.children.length === 1 && d.children[0] && (g = d.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Po(o, g), t && g.classList.add(...t.split(" ")), r) {
        const m = Ro(r);
        Object.keys(m).forEach((x) => {
          g.style[x] = m[x];
        });
      }
    }
    let p = null, b = null;
    if (u && window.MutationObserver) {
      let g = function() {
        var y, C, S;
        (y = s.current) != null && y.contains(d) && ((C = s.current) == null || C.removeChild(d));
        const {
          portals: x,
          clonedElement: _
        } = qt(n);
        d = _, c(x), d.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          h();
        }, 50), (S = s.current) == null || S.appendChild(d);
      };
      g();
      const m = Yi(() => {
        g(), p == null || p.disconnect(), p == null || p.observe(n, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      p = new window.MutationObserver(m), p.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      d.style.display = "contents", h(), (v = s.current) == null || v.appendChild(d);
    return () => {
      var g, m;
      d.style.display = "", (g = s.current) != null && g.contains(d) && ((m = s.current) == null || m.removeChild(d)), p == null || p.disconnect();
    };
  }, [n, u, t, r, o, i, l]), f.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Mo = "1.1.0", Lo = /* @__PURE__ */ f.createContext({}), Oo = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, fr = (n) => {
  const e = f.useContext(Lo);
  return f.useMemo(() => ({
    ...Oo,
    ...e[n]
  }), [e[n]]);
};
function ge() {
  return ge = Object.assign ? Object.assign.bind() : function(n) {
    for (var e = 1; e < arguments.length; e++) {
      var t = arguments[e];
      for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]);
    }
    return n;
  }, ge.apply(null, arguments);
}
function Ve() {
  const {
    getPrefixCls: n,
    direction: e,
    csp: t,
    iconPrefixCls: r,
    theme: i
  } = f.useContext(Mi.ConfigContext);
  return {
    theme: i,
    getPrefixCls: n,
    direction: e,
    csp: t,
    iconPrefixCls: r
  };
}
function Ee(n) {
  var e = R.useRef();
  e.current = n;
  var t = R.useCallback(function() {
    for (var r, i = arguments.length, o = new Array(i), s = 0; s < i; s++)
      o[s] = arguments[s];
    return (r = e.current) === null || r === void 0 ? void 0 : r.call.apply(r, [e].concat(o));
  }, []);
  return t;
}
function Ao(n) {
  if (Array.isArray(n)) return n;
}
function $o(n, e) {
  var t = n == null ? null : typeof Symbol < "u" && n[Symbol.iterator] || n["@@iterator"];
  if (t != null) {
    var r, i, o, s, a = [], c = !0, l = !1;
    try {
      if (o = (t = t.call(n)).next, e === 0) {
        if (Object(t) !== t) return;
        c = !1;
      } else for (; !(c = (r = o.call(t)).done) && (a.push(r.value), a.length !== e); c = !0) ;
    } catch (u) {
      l = !0, i = u;
    } finally {
      try {
        if (!c && t.return != null && (s = t.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw i;
      }
    }
    return a;
  }
}
function _n(n, e) {
  (e == null || e > n.length) && (e = n.length);
  for (var t = 0, r = Array(e); t < e; t++) r[t] = n[t];
  return r;
}
function Io(n, e) {
  if (n) {
    if (typeof n == "string") return _n(n, e);
    var t = {}.toString.call(n).slice(8, -1);
    return t === "Object" && n.constructor && (t = n.constructor.name), t === "Map" || t === "Set" ? Array.from(n) : t === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _n(n, e) : void 0;
  }
}
function ko() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ce(n, e) {
  return Ao(n) || $o(n, e) || Io(n, e) || ko();
}
function pt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Rn = pt() ? R.useLayoutEffect : R.useEffect, Do = function(e, t) {
  var r = R.useRef(!0);
  Rn(function() {
    return e(r.current);
  }, t), Rn(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, Tn = function(e, t) {
  Do(function(r) {
    if (!r)
      return e();
  }, t);
};
function Ue(n) {
  var e = R.useRef(!1), t = R.useState(n), r = ce(t, 2), i = r[0], o = r[1];
  R.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, c) {
    c && e.current || o(a);
  }
  return [i, s];
}
function It(n) {
  return n !== void 0;
}
function an(n, e) {
  var t = e || {}, r = t.defaultValue, i = t.value, o = t.onChange, s = t.postState, a = Ue(function() {
    return It(i) ? i : It(r) ? typeof r == "function" ? r() : r : typeof n == "function" ? n() : n;
  }), c = ce(a, 2), l = c[0], u = c[1], d = i !== void 0 ? i : l, h = s ? s(d) : d, p = Ee(o), b = Ue([d]), v = ce(b, 2), g = v[0], m = v[1];
  Tn(function() {
    var _ = g[0];
    l !== _ && p(l, _);
  }, [g]), Tn(function() {
    It(i) || u(i);
  }, [i]);
  var x = Ee(function(_, y) {
    u(_, y), m([d], y);
  });
  return [h, x];
}
function oe(n) {
  "@babel/helpers - typeof";
  return oe = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, oe(n);
}
var hr = {
  exports: {}
}, B = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ln = Symbol.for("react.element"), cn = Symbol.for("react.portal"), mt = Symbol.for("react.fragment"), gt = Symbol.for("react.strict_mode"), vt = Symbol.for("react.profiler"), bt = Symbol.for("react.provider"), yt = Symbol.for("react.context"), No = Symbol.for("react.server_context"), wt = Symbol.for("react.forward_ref"), St = Symbol.for("react.suspense"), xt = Symbol.for("react.suspense_list"), Ct = Symbol.for("react.memo"), Et = Symbol.for("react.lazy"), Fo = Symbol.for("react.offscreen"), pr;
pr = Symbol.for("react.module.reference");
function ve(n) {
  if (typeof n == "object" && n !== null) {
    var e = n.$$typeof;
    switch (e) {
      case ln:
        switch (n = n.type, n) {
          case mt:
          case vt:
          case gt:
          case St:
          case xt:
            return n;
          default:
            switch (n = n && n.$$typeof, n) {
              case No:
              case yt:
              case wt:
              case Et:
              case Ct:
              case bt:
                return n;
              default:
                return e;
            }
        }
      case cn:
        return e;
    }
  }
}
B.ContextConsumer = yt;
B.ContextProvider = bt;
B.Element = ln;
B.ForwardRef = wt;
B.Fragment = mt;
B.Lazy = Et;
B.Memo = Ct;
B.Portal = cn;
B.Profiler = vt;
B.StrictMode = gt;
B.Suspense = St;
B.SuspenseList = xt;
B.isAsyncMode = function() {
  return !1;
};
B.isConcurrentMode = function() {
  return !1;
};
B.isContextConsumer = function(n) {
  return ve(n) === yt;
};
B.isContextProvider = function(n) {
  return ve(n) === bt;
};
B.isElement = function(n) {
  return typeof n == "object" && n !== null && n.$$typeof === ln;
};
B.isForwardRef = function(n) {
  return ve(n) === wt;
};
B.isFragment = function(n) {
  return ve(n) === mt;
};
B.isLazy = function(n) {
  return ve(n) === Et;
};
B.isMemo = function(n) {
  return ve(n) === Ct;
};
B.isPortal = function(n) {
  return ve(n) === cn;
};
B.isProfiler = function(n) {
  return ve(n) === vt;
};
B.isStrictMode = function(n) {
  return ve(n) === gt;
};
B.isSuspense = function(n) {
  return ve(n) === St;
};
B.isSuspenseList = function(n) {
  return ve(n) === xt;
};
B.isValidElementType = function(n) {
  return typeof n == "string" || typeof n == "function" || n === mt || n === vt || n === gt || n === St || n === xt || n === Fo || typeof n == "object" && n !== null && (n.$$typeof === Et || n.$$typeof === Ct || n.$$typeof === bt || n.$$typeof === yt || n.$$typeof === wt || n.$$typeof === pr || n.getModuleId !== void 0);
};
B.typeOf = ve;
hr.exports = B;
var kt = hr.exports, Wo = Symbol.for("react.element"), jo = Symbol.for("react.transitional.element"), Bo = Symbol.for("react.fragment");
function Ho(n) {
  return (
    // Base object type
    n && oe(n) === "object" && // React Element type
    (n.$$typeof === Wo || n.$$typeof === jo) && // React Fragment type
    n.type === Bo
  );
}
var zo = Number(qr.split(".")[0]), Vo = function(e, t) {
  typeof e == "function" ? e(t) : oe(e) === "object" && e && "current" in e && (e.current = t);
}, Uo = function(e) {
  var t, r;
  if (!e)
    return !1;
  if (mr(e) && zo >= 19)
    return !0;
  var i = kt.isMemo(e) ? e.type.type : e.type;
  return !(typeof i == "function" && !((t = i.prototype) !== null && t !== void 0 && t.render) && i.$$typeof !== kt.ForwardRef || typeof e == "function" && !((r = e.prototype) !== null && r !== void 0 && r.render) && e.$$typeof !== kt.ForwardRef);
};
function mr(n) {
  return /* @__PURE__ */ Kr(n) && !Ho(n);
}
var Xo = function(e) {
  if (e && mr(e)) {
    var t = e;
    return t.props.propertyIsEnumerable("ref") ? t.props.ref : t.ref;
  }
  return null;
};
function Go(n, e) {
  for (var t = n, r = 0; r < e.length; r += 1) {
    if (t == null)
      return;
    t = t[e[r]];
  }
  return t;
}
function qo(n, e) {
  if (oe(n) != "object" || !n) return n;
  var t = n[Symbol.toPrimitive];
  if (t !== void 0) {
    var r = t.call(n, e);
    if (oe(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(n);
}
function gr(n) {
  var e = qo(n, "string");
  return oe(e) == "symbol" ? e : e + "";
}
function I(n, e, t) {
  return (e = gr(e)) in n ? Object.defineProperty(n, e, {
    value: t,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : n[e] = t, n;
}
function Pn(n, e) {
  var t = Object.keys(n);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(n);
    e && (r = r.filter(function(i) {
      return Object.getOwnPropertyDescriptor(n, i).enumerable;
    })), t.push.apply(t, r);
  }
  return t;
}
function A(n) {
  for (var e = 1; e < arguments.length; e++) {
    var t = arguments[e] != null ? arguments[e] : {};
    e % 2 ? Pn(Object(t), !0).forEach(function(r) {
      I(n, r, t[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(n, Object.getOwnPropertyDescriptors(t)) : Pn(Object(t)).forEach(function(r) {
      Object.defineProperty(n, r, Object.getOwnPropertyDescriptor(t, r));
    });
  }
  return n;
}
const Xe = /* @__PURE__ */ f.createContext(null);
function Mn(n) {
  const {
    getDropContainer: e,
    className: t,
    prefixCls: r,
    children: i
  } = n, {
    disabled: o
  } = f.useContext(Xe), [s, a] = f.useState(), [c, l] = f.useState(null);
  if (f.useEffect(() => {
    const h = e == null ? void 0 : e();
    s !== h && a(h);
  }, [e]), f.useEffect(() => {
    if (s) {
      const h = () => {
        l(!0);
      }, p = (g) => {
        g.preventDefault();
      }, b = (g) => {
        g.relatedTarget || l(!1);
      }, v = (g) => {
        l(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", h), document.addEventListener("dragover", p), document.addEventListener("dragleave", b), document.addEventListener("drop", v), () => {
        document.removeEventListener("dragenter", h), document.removeEventListener("dragover", p), document.removeEventListener("dragleave", b), document.removeEventListener("drop", v);
      };
    }
  }, [!!s]), !(e && s && !o))
    return null;
  const d = `${r}-drop-area`;
  return /* @__PURE__ */ ut(/* @__PURE__ */ f.createElement("div", {
    className: J(d, t, {
      [`${d}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, i), s);
}
function Ln(n) {
  return n instanceof HTMLElement || n instanceof SVGElement;
}
function Ko(n) {
  return n && oe(n) === "object" && Ln(n.nativeElement) ? n.nativeElement : Ln(n) ? n : null;
}
function Yo(n) {
  var e = Ko(n);
  if (e)
    return e;
  if (n instanceof f.Component) {
    var t;
    return (t = hn.findDOMNode) === null || t === void 0 ? void 0 : t.call(hn, n);
  }
  return null;
}
function Zo(n, e) {
  if (n == null) return {};
  var t = {};
  for (var r in n) if ({}.hasOwnProperty.call(n, r)) {
    if (e.indexOf(r) !== -1) continue;
    t[r] = n[r];
  }
  return t;
}
function On(n, e) {
  if (n == null) return {};
  var t, r, i = Zo(n, e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(n);
    for (r = 0; r < o.length; r++) t = o[r], e.indexOf(t) === -1 && {}.propertyIsEnumerable.call(n, t) && (i[t] = n[t]);
  }
  return i;
}
var Qo = /* @__PURE__ */ R.createContext({});
function Ie(n, e) {
  if (!(n instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function An(n, e) {
  for (var t = 0; t < e.length; t++) {
    var r = e[t];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(n, gr(r.key), r);
  }
}
function ke(n, e, t) {
  return e && An(n.prototype, e), t && An(n, t), Object.defineProperty(n, "prototype", {
    writable: !1
  }), n;
}
function Yt(n, e) {
  return Yt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(t, r) {
    return t.__proto__ = r, t;
  }, Yt(n, e);
}
function _t(n, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  n.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: n,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(n, "prototype", {
    writable: !1
  }), e && Yt(n, e);
}
function dt(n) {
  return dt = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, dt(n);
}
function vr() {
  try {
    var n = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (vr = function() {
    return !!n;
  })();
}
function Re(n) {
  if (n === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return n;
}
function Jo(n, e) {
  if (e && (oe(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Re(n);
}
function Rt(n) {
  var e = vr();
  return function() {
    var t, r = dt(n);
    if (e) {
      var i = dt(this).constructor;
      t = Reflect.construct(r, arguments, i);
    } else t = r.apply(this, arguments);
    return Jo(this, t);
  };
}
var es = /* @__PURE__ */ function(n) {
  _t(t, n);
  var e = Rt(t);
  function t() {
    return Ie(this, t), e.apply(this, arguments);
  }
  return ke(t, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), t;
}(R.Component);
function ts(n) {
  var e = R.useReducer(function(a) {
    return a + 1;
  }, 0), t = ce(e, 2), r = t[1], i = R.useRef(n), o = Ee(function() {
    return i.current;
  }), s = Ee(function(a) {
    i.current = typeof a == "function" ? a(i.current) : a, r();
  });
  return [o, s];
}
var Ce = "none", Ke = "appear", Ye = "enter", Ze = "leave", $n = "none", be = "prepare", Le = "start", Oe = "active", un = "end", br = "prepared";
function In(n, e) {
  var t = {};
  return t[n.toLowerCase()] = e.toLowerCase(), t["Webkit".concat(n)] = "webkit".concat(e), t["Moz".concat(n)] = "moz".concat(e), t["ms".concat(n)] = "MS".concat(e), t["O".concat(n)] = "o".concat(e.toLowerCase()), t;
}
function ns(n, e) {
  var t = {
    animationend: In("Animation", "AnimationEnd"),
    transitionend: In("Transition", "TransitionEnd")
  };
  return n && ("AnimationEvent" in e || delete t.animationend.animation, "TransitionEvent" in e || delete t.transitionend.transition), t;
}
var rs = ns(pt(), typeof window < "u" ? window : {}), yr = {};
if (pt()) {
  var is = document.createElement("div");
  yr = is.style;
}
var Qe = {};
function wr(n) {
  if (Qe[n])
    return Qe[n];
  var e = rs[n];
  if (e)
    for (var t = Object.keys(e), r = t.length, i = 0; i < r; i += 1) {
      var o = t[i];
      if (Object.prototype.hasOwnProperty.call(e, o) && o in yr)
        return Qe[n] = e[o], Qe[n];
    }
  return "";
}
var Sr = wr("animationend"), xr = wr("transitionend"), Cr = !!(Sr && xr), kn = Sr || "animationend", Dn = xr || "transitionend";
function Nn(n, e) {
  if (!n) return null;
  if (oe(n) === "object") {
    var t = e.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return n[t];
  }
  return "".concat(n, "-").concat(e);
}
const os = function(n) {
  var e = de();
  function t(i) {
    i && (i.removeEventListener(Dn, n), i.removeEventListener(kn, n));
  }
  function r(i) {
    e.current && e.current !== i && t(e.current), i && i !== e.current && (i.addEventListener(Dn, n), i.addEventListener(kn, n), e.current = i);
  }
  return R.useEffect(function() {
    return function() {
      t(e.current);
    };
  }, []), [r, t];
};
var Er = pt() ? Yr : Se, _r = function(e) {
  return +setTimeout(e, 16);
}, Rr = function(e) {
  return clearTimeout(e);
};
typeof window < "u" && "requestAnimationFrame" in window && (_r = function(e) {
  return window.requestAnimationFrame(e);
}, Rr = function(e) {
  return window.cancelAnimationFrame(e);
});
var Fn = 0, dn = /* @__PURE__ */ new Map();
function Tr(n) {
  dn.delete(n);
}
var Zt = function(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  Fn += 1;
  var r = Fn;
  function i(o) {
    if (o === 0)
      Tr(r), e();
    else {
      var s = _r(function() {
        i(o - 1);
      });
      dn.set(r, s);
    }
  }
  return i(t), r;
};
Zt.cancel = function(n) {
  var e = dn.get(n);
  return Tr(n), Rr(e);
};
const ss = function() {
  var n = R.useRef(null);
  function e() {
    Zt.cancel(n.current);
  }
  function t(r) {
    var i = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    e();
    var o = Zt(function() {
      i <= 1 ? r({
        isCanceled: function() {
          return o !== n.current;
        }
      }) : t(r, i - 1);
    });
    n.current = o;
  }
  return R.useEffect(function() {
    return function() {
      e();
    };
  }, []), [t, e];
};
var as = [be, Le, Oe, un], ls = [be, br], Pr = !1, cs = !0;
function Mr(n) {
  return n === Oe || n === un;
}
const us = function(n, e, t) {
  var r = Ue($n), i = ce(r, 2), o = i[0], s = i[1], a = ss(), c = ce(a, 2), l = c[0], u = c[1];
  function d() {
    s(be, !0);
  }
  var h = e ? ls : as;
  return Er(function() {
    if (o !== $n && o !== un) {
      var p = h.indexOf(o), b = h[p + 1], v = t(o);
      v === Pr ? s(b, !0) : b && l(function(g) {
        function m() {
          g.isCanceled() || s(b, !0);
        }
        v === !0 ? m() : Promise.resolve(v).then(m);
      });
    }
  }, [n, o]), R.useEffect(function() {
    return function() {
      u();
    };
  }, []), [d, o];
};
function ds(n, e, t, r) {
  var i = r.motionEnter, o = i === void 0 ? !0 : i, s = r.motionAppear, a = s === void 0 ? !0 : s, c = r.motionLeave, l = c === void 0 ? !0 : c, u = r.motionDeadline, d = r.motionLeaveImmediately, h = r.onAppearPrepare, p = r.onEnterPrepare, b = r.onLeavePrepare, v = r.onAppearStart, g = r.onEnterStart, m = r.onLeaveStart, x = r.onAppearActive, _ = r.onEnterActive, y = r.onLeaveActive, C = r.onAppearEnd, S = r.onEnterEnd, T = r.onLeaveEnd, E = r.onVisibleChanged, P = Ue(), $ = ce(P, 2), k = $[0], D = $[1], N = ts(Ce), F = ce(N, 2), L = F[0], M = F[1], z = Ue(null), w = ce(z, 2), fe = w[0], he = w[1], V = L(), W = de(!1), Z = de(null);
  function X() {
    return t();
  }
  var ee = de(!1);
  function re() {
    M(Ce), he(null, !0);
  }
  var j = Ee(function(se) {
    var te = L();
    if (te !== Ce) {
      var ae = X();
      if (!(se && !se.deadline && se.target !== ae)) {
        var Te = ee.current, we;
        te === Ke && Te ? we = C == null ? void 0 : C(ae, se) : te === Ye && Te ? we = S == null ? void 0 : S(ae, se) : te === Ze && Te && (we = T == null ? void 0 : T(ae, se)), Te && we !== !1 && re();
      }
    }
  }), O = os(j), H = ce(O, 1), ie = H[0], G = function(te) {
    switch (te) {
      case Ke:
        return I(I(I({}, be, h), Le, v), Oe, x);
      case Ye:
        return I(I(I({}, be, p), Le, g), Oe, _);
      case Ze:
        return I(I(I({}, be, b), Le, m), Oe, y);
      default:
        return {};
    }
  }, U = R.useMemo(function() {
    return G(V);
  }, [V]), me = us(V, !n, function(se) {
    if (se === be) {
      var te = U[be];
      return te ? te(X()) : Pr;
    }
    if (ue in U) {
      var ae;
      he(((ae = U[ue]) === null || ae === void 0 ? void 0 : ae.call(U, X(), null)) || null);
    }
    return ue === Oe && V !== Ce && (ie(X()), u > 0 && (clearTimeout(Z.current), Z.current = setTimeout(function() {
      j({
        deadline: !0
      });
    }, u))), ue === br && re(), cs;
  }), pe = ce(me, 2), K = pe[0], ue = pe[1], xe = Mr(ue);
  ee.current = xe;
  var Q = de(null);
  Er(function() {
    if (!(W.current && Q.current === e)) {
      D(e);
      var se = W.current;
      W.current = !0;
      var te;
      !se && e && a && (te = Ke), se && e && o && (te = Ye), (se && !e && l || !se && d && !e && l) && (te = Ze);
      var ae = G(te);
      te && (n || ae[be]) ? (M(te), K()) : M(Ce), Q.current = e;
    }
  }, [e]), Se(function() {
    // Cancel appear
    (V === Ke && !a || // Cancel enter
    V === Ye && !o || // Cancel leave
    V === Ze && !l) && M(Ce);
  }, [a, o, l]), Se(function() {
    return function() {
      W.current = !1, clearTimeout(Z.current);
    };
  }, []);
  var _e = R.useRef(!1);
  Se(function() {
    k && (_e.current = !0), k !== void 0 && V === Ce && ((_e.current || k) && (E == null || E(k)), _e.current = !0);
  }, [k, V]);
  var De = fe;
  return U[be] && ue === Le && (De = A({
    transition: "none"
  }, De)), [V, ue, De, k ?? e];
}
function fs(n) {
  var e = n;
  oe(n) === "object" && (e = n.transitionSupport);
  function t(i, o) {
    return !!(i.motionName && e && o !== !1);
  }
  var r = /* @__PURE__ */ R.forwardRef(function(i, o) {
    var s = i.visible, a = s === void 0 ? !0 : s, c = i.removeOnLeave, l = c === void 0 ? !0 : c, u = i.forceRender, d = i.children, h = i.motionName, p = i.leavedClassName, b = i.eventProps, v = R.useContext(Qo), g = v.motion, m = t(i, g), x = de(), _ = de();
    function y() {
      try {
        return x.current instanceof HTMLElement ? x.current : Yo(_.current);
      } catch {
        return null;
      }
    }
    var C = ds(m, a, y, i), S = ce(C, 4), T = S[0], E = S[1], P = S[2], $ = S[3], k = R.useRef($);
    $ && (k.current = !0);
    var D = R.useCallback(function(w) {
      x.current = w, Vo(o, w);
    }, [o]), N, F = A(A({}, b), {}, {
      visible: a
    });
    if (!d)
      N = null;
    else if (T === Ce)
      $ ? N = d(A({}, F), D) : !l && k.current && p ? N = d(A(A({}, F), {}, {
        className: p
      }), D) : u || !l && !p ? N = d(A(A({}, F), {}, {
        style: {
          display: "none"
        }
      }), D) : N = null;
    else {
      var L;
      E === be ? L = "prepare" : Mr(E) ? L = "active" : E === Le && (L = "start");
      var M = Nn(h, "".concat(T, "-").concat(L));
      N = d(A(A({}, F), {}, {
        className: J(Nn(h, T), I(I({}, M, M && L), h, typeof h == "string")),
        style: P
      }), D);
    }
    if (/* @__PURE__ */ R.isValidElement(N) && Uo(N)) {
      var z = Xo(N);
      z || (N = /* @__PURE__ */ R.cloneElement(N, {
        ref: D
      }));
    }
    return /* @__PURE__ */ R.createElement(es, {
      ref: _
    }, N);
  });
  return r.displayName = "CSSMotion", r;
}
const Lr = fs(Cr);
var Qt = "add", Jt = "keep", en = "remove", Dt = "removed";
function hs(n) {
  var e;
  return n && oe(n) === "object" && "key" in n ? e = n : e = {
    key: n
  }, A(A({}, e), {}, {
    key: String(e.key)
  });
}
function tn() {
  var n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return n.map(hs);
}
function ps() {
  var n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], t = [], r = 0, i = e.length, o = tn(n), s = tn(e);
  o.forEach(function(l) {
    for (var u = !1, d = r; d < i; d += 1) {
      var h = s[d];
      if (h.key === l.key) {
        r < d && (t = t.concat(s.slice(r, d).map(function(p) {
          return A(A({}, p), {}, {
            status: Qt
          });
        })), r = d), t.push(A(A({}, h), {}, {
          status: Jt
        })), r += 1, u = !0;
        break;
      }
    }
    u || t.push(A(A({}, l), {}, {
      status: en
    }));
  }), r < i && (t = t.concat(s.slice(r).map(function(l) {
    return A(A({}, l), {}, {
      status: Qt
    });
  })));
  var a = {};
  t.forEach(function(l) {
    var u = l.key;
    a[u] = (a[u] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(l) {
    return a[l] > 1;
  });
  return c.forEach(function(l) {
    t = t.filter(function(u) {
      var d = u.key, h = u.status;
      return d !== l || h !== en;
    }), t.forEach(function(u) {
      u.key === l && (u.status = Jt);
    });
  }), t;
}
var ms = ["component", "children", "onVisibleChanged", "onAllRemoved"], gs = ["status"], vs = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function bs(n) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Lr, t = /* @__PURE__ */ function(r) {
    _t(o, r);
    var i = Rt(o);
    function o() {
      var s;
      Ie(this, o);
      for (var a = arguments.length, c = new Array(a), l = 0; l < a; l++)
        c[l] = arguments[l];
      return s = i.call.apply(i, [this].concat(c)), I(Re(s), "state", {
        keyEntities: []
      }), I(Re(s), "removeKey", function(u) {
        s.setState(function(d) {
          var h = d.keyEntities.map(function(p) {
            return p.key !== u ? p : A(A({}, p), {}, {
              status: Dt
            });
          });
          return {
            keyEntities: h
          };
        }, function() {
          var d = s.state.keyEntities, h = d.filter(function(p) {
            var b = p.status;
            return b !== Dt;
          }).length;
          h === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return ke(o, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, l = this.props, u = l.component, d = l.children, h = l.onVisibleChanged;
        l.onAllRemoved;
        var p = On(l, ms), b = u || R.Fragment, v = {};
        return vs.forEach(function(g) {
          v[g] = p[g], delete p[g];
        }), delete p.keys, /* @__PURE__ */ R.createElement(b, p, c.map(function(g, m) {
          var x = g.status, _ = On(g, gs), y = x === Qt || x === Jt;
          return /* @__PURE__ */ R.createElement(e, ge({}, v, {
            key: _.key,
            visible: y,
            eventProps: _,
            onVisibleChanged: function(S) {
              h == null || h(S, {
                key: _.key
              }), S || a.removeKey(_.key);
            }
          }), function(C, S) {
            return d(A(A({}, C), {}, {
              index: m
            }), S);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var l = a.keys, u = c.keyEntities, d = tn(l), h = ps(u, d);
        return {
          keyEntities: h.filter(function(p) {
            var b = u.find(function(v) {
              var g = v.key;
              return p.key === g;
            });
            return !(b && b.status === Dt && p.status === en);
          })
        };
      }
    }]), o;
  }(R.Component);
  return I(t, "defaultProps", {
    component: "div"
  }), t;
}
const ys = bs(Cr);
function ws(n, e) {
  const {
    children: t,
    upload: r,
    rootClassName: i
  } = n, o = f.useRef(null);
  return f.useImperativeHandle(e, () => o.current), /* @__PURE__ */ f.createElement(ir, ge({}, r, {
    showUploadList: !1,
    rootClassName: i,
    ref: o
  }), t);
}
const Or = /* @__PURE__ */ f.forwardRef(ws);
var Ar = /* @__PURE__ */ ke(function n() {
  Ie(this, n);
}), $r = "CALC_UNIT", Ss = new RegExp($r, "g");
function Nt(n) {
  return typeof n == "number" ? "".concat(n).concat($r) : n;
}
var xs = /* @__PURE__ */ function(n) {
  _t(t, n);
  var e = Rt(t);
  function t(r, i) {
    var o;
    Ie(this, t), o = e.call(this), I(Re(o), "result", ""), I(Re(o), "unitlessCssVar", void 0), I(Re(o), "lowPriority", void 0);
    var s = oe(r);
    return o.unitlessCssVar = i, r instanceof t ? o.result = "(".concat(r.result, ")") : s === "number" ? o.result = Nt(r) : s === "string" && (o.result = r), o;
  }
  return ke(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " + ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " + ").concat(Nt(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " - ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " - ").concat(Nt(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " * ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " * ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " / ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " / ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(i) {
      return this.lowPriority || i ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(i) {
      var o = this, s = i || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return o.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(Ss, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), t;
}(Ar), Cs = /* @__PURE__ */ function(n) {
  _t(t, n);
  var e = Rt(t);
  function t(r) {
    var i;
    return Ie(this, t), i = e.call(this), I(Re(i), "result", 0), r instanceof t ? i.result = r.result : typeof r == "number" && (i.result = r), i;
  }
  return ke(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result += i.result : typeof i == "number" && (this.result += i), this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result -= i.result : typeof i == "number" && (this.result -= i), this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return i instanceof t ? this.result *= i.result : typeof i == "number" && (this.result *= i), this;
    }
  }, {
    key: "div",
    value: function(i) {
      return i instanceof t ? this.result /= i.result : typeof i == "number" && (this.result /= i), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), t;
}(Ar), Es = function(e, t) {
  var r = e === "css" ? xs : Cs;
  return function(i) {
    return new r(i, t);
  };
}, Wn = function(e, t) {
  return "".concat([t, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function jn(n, e, t, r) {
  var i = A({}, e[n]);
  if (r != null && r.deprecatedTokens) {
    var o = r.deprecatedTokens;
    o.forEach(function(a) {
      var c = ce(a, 2), l = c[0], u = c[1];
      if (i != null && i[l] || i != null && i[u]) {
        var d;
        (d = i[u]) !== null && d !== void 0 || (i[u] = i == null ? void 0 : i[l]);
      }
    });
  }
  var s = A(A({}, t), i);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Ir = typeof CSSINJS_STATISTIC < "u", nn = !0;
function Tt() {
  for (var n = arguments.length, e = new Array(n), t = 0; t < n; t++)
    e[t] = arguments[t];
  if (!Ir)
    return Object.assign.apply(Object, [{}].concat(e));
  nn = !1;
  var r = {};
  return e.forEach(function(i) {
    if (oe(i) === "object") {
      var o = Object.keys(i);
      o.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return i[s];
          }
        });
      });
    }
  }), nn = !0, r;
}
var Bn = {};
function _s() {
}
var Rs = function(e) {
  var t, r = e, i = _s;
  return Ir && typeof Proxy < "u" && (t = /* @__PURE__ */ new Set(), r = new Proxy(e, {
    get: function(s, a) {
      if (nn) {
        var c;
        (c = t) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), i = function(s, a) {
    var c;
    Bn[s] = {
      global: Array.from(t),
      component: A(A({}, (c = Bn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: r,
    keys: t,
    flush: i
  };
};
function Hn(n, e, t) {
  if (typeof t == "function") {
    var r;
    return t(Tt(e, (r = e[n]) !== null && r !== void 0 ? r : {}));
  }
  return t ?? {};
}
function Ts(n) {
  return n === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var t = arguments.length, r = new Array(t), i = 0; i < t; i++)
        r[i] = arguments[i];
      return "max(".concat(r.map(function(o) {
        return Xt(o);
      }).join(","), ")");
    },
    min: function() {
      for (var t = arguments.length, r = new Array(t), i = 0; i < t; i++)
        r[i] = arguments[i];
      return "min(".concat(r.map(function(o) {
        return Xt(o);
      }).join(","), ")");
    }
  };
}
var Ps = 1e3 * 60 * 10, Ms = /* @__PURE__ */ function() {
  function n() {
    Ie(this, n), I(this, "map", /* @__PURE__ */ new Map()), I(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), I(this, "nextID", 0), I(this, "lastAccessBeat", /* @__PURE__ */ new Map()), I(this, "accessBeat", 0);
  }
  return ke(n, [{
    key: "set",
    value: function(t, r) {
      this.clear();
      var i = this.getCompositeKey(t);
      this.map.set(i, r), this.lastAccessBeat.set(i, Date.now());
    }
  }, {
    key: "get",
    value: function(t) {
      var r = this.getCompositeKey(t), i = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, i;
    }
  }, {
    key: "getCompositeKey",
    value: function(t) {
      var r = this, i = t.map(function(o) {
        return o && oe(o) === "object" ? "obj_".concat(r.getObjectID(o)) : "".concat(oe(o), "_").concat(o);
      });
      return i.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(t) {
      if (this.objectIDMap.has(t))
        return this.objectIDMap.get(t);
      var r = this.nextID;
      return this.objectIDMap.set(t, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var t = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(i, o) {
          r - i > Ps && (t.map.delete(o), t.lastAccessBeat.delete(o));
        }), this.accessBeat = 0;
      }
    }
  }]), n;
}(), zn = new Ms();
function Ls(n, e) {
  return f.useMemo(function() {
    var t = zn.get(e);
    if (t)
      return t;
    var r = n();
    return zn.set(e, r), r;
  }, e);
}
var Os = function() {
  return {};
};
function As(n) {
  var e = n.useCSP, t = e === void 0 ? Os : e, r = n.useToken, i = n.usePrefix, o = n.getResetStyles, s = n.getCommonStyle, a = n.getCompUnitless;
  function c(h, p, b, v) {
    var g = Array.isArray(h) ? h[0] : h;
    function m(E) {
      return "".concat(String(g)).concat(E.slice(0, 1).toUpperCase()).concat(E.slice(1));
    }
    var x = (v == null ? void 0 : v.unitless) || {}, _ = typeof a == "function" ? a(h) : {}, y = A(A({}, _), {}, I({}, m("zIndexPopup"), !0));
    Object.keys(x).forEach(function(E) {
      y[m(E)] = x[E];
    });
    var C = A(A({}, v), {}, {
      unitless: y,
      prefixToken: m
    }), S = u(h, p, b, C), T = l(g, b, C);
    return function(E) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, $ = S(E, P), k = ce($, 2), D = k[1], N = T(P), F = ce(N, 2), L = F[0], M = F[1];
      return [L, D, M];
    };
  }
  function l(h, p, b) {
    var v = b.unitless, g = b.injectStyle, m = g === void 0 ? !0 : g, x = b.prefixToken, _ = b.ignore, y = function(T) {
      var E = T.rootCls, P = T.cssVar, $ = P === void 0 ? {} : P, k = r(), D = k.realToken;
      return ki({
        path: [h],
        prefix: $.prefix,
        key: $.key,
        unitless: v,
        ignore: _,
        token: D,
        scope: E
      }, function() {
        var N = Hn(h, D, p), F = jn(h, D, N, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(N).forEach(function(L) {
          F[x(L)] = F[L], delete F[L];
        }), F;
      }), null;
    }, C = function(T) {
      var E = r(), P = E.cssVar;
      return [function($) {
        return m && P ? /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(y, {
          rootCls: T,
          cssVar: P,
          component: h
        }), $) : $;
      }, P == null ? void 0 : P.key];
    };
    return C;
  }
  function u(h, p, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(h) ? h : [h, h], m = ce(g, 1), x = m[0], _ = g.join("-"), y = n.layer || {
      name: "antd"
    };
    return function(C) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, T = r(), E = T.theme, P = T.realToken, $ = T.hashId, k = T.token, D = T.cssVar, N = i(), F = N.rootPrefixCls, L = N.iconPrefixCls, M = t(), z = D ? "css" : "js", w = Ls(function() {
        var X = /* @__PURE__ */ new Set();
        return D && Object.keys(v.unitless || {}).forEach(function(ee) {
          X.add(Ot(ee, D.prefix)), X.add(Ot(ee, Wn(x, D.prefix)));
        }), Es(z, X);
      }, [z, x, D == null ? void 0 : D.prefix]), fe = Ts(z), he = fe.max, V = fe.min, W = {
        theme: E,
        token: k,
        hashId: $,
        nonce: function() {
          return M.nonce;
        },
        clientOnly: v.clientOnly,
        layer: y,
        // antd is always at top of styles
        order: v.order || -999
      };
      typeof o == "function" && pn(A(A({}, W), {}, {
        clientOnly: !1,
        path: ["Shared", F]
      }), function() {
        return o(k, {
          prefix: {
            rootPrefixCls: F,
            iconPrefixCls: L
          },
          csp: M
        });
      });
      var Z = pn(A(A({}, W), {}, {
        path: [_, C, L]
      }), function() {
        if (v.injectStyle === !1)
          return [];
        var X = Rs(k), ee = X.token, re = X.flush, j = Hn(x, P, b), O = ".".concat(C), H = jn(x, P, j, {
          deprecatedTokens: v.deprecatedTokens
        });
        D && j && oe(j) === "object" && Object.keys(j).forEach(function(me) {
          j[me] = "var(".concat(Ot(me, Wn(x, D.prefix)), ")");
        });
        var ie = Tt(ee, {
          componentCls: O,
          prefixCls: C,
          iconCls: ".".concat(L),
          antCls: ".".concat(F),
          calc: w,
          // @ts-ignore
          max: he,
          // @ts-ignore
          min: V
        }, D ? j : H), G = p(ie, {
          hashId: $,
          prefixCls: C,
          rootPrefixCls: F,
          iconPrefixCls: L
        });
        re(x, H);
        var U = typeof s == "function" ? s(ie, C, S, v.resetFont) : null;
        return [v.resetStyle === !1 ? null : U, G];
      });
      return [Z, $];
    };
  }
  function d(h, p, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = u(h, p, b, A({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, v)), m = function(_) {
      var y = _.prefixCls, C = _.rootCls, S = C === void 0 ? y : C;
      return g(y, S), null;
    };
    return m;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: d,
    genComponentStyleHook: u
  };
}
const ne = Math.round;
function Ft(n, e) {
  const t = n.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = t.map((i) => parseFloat(i));
  for (let i = 0; i < 3; i += 1)
    r[i] = e(r[i] || 0, t[i] || "", i);
  return t[3] ? r[3] = t[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const Vn = (n, e, t) => t === 0 ? n : n / 100;
function Fe(n, e) {
  const t = e || 255;
  return n > t ? t : n < 0 ? 0 : n;
}
class ye {
  constructor(e) {
    I(this, "isValid", !0), I(this, "r", 0), I(this, "g", 0), I(this, "b", 0), I(this, "a", 1), I(this, "_h", void 0), I(this, "_s", void 0), I(this, "_l", void 0), I(this, "_v", void 0), I(this, "_max", void 0), I(this, "_min", void 0), I(this, "_brightness", void 0);
    function t(r) {
      return r[0] in e && r[1] in e && r[2] in e;
    }
    if (e) if (typeof e == "string") {
      let i = function(o) {
        return r.startsWith(o);
      };
      const r = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : i("rgb") ? this.fromRgbString(r) : i("hsl") ? this.fromHslString(r) : (i("hsv") || i("hsb")) && this.fromHsvString(r);
    } else if (e instanceof ye)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (t("rgb"))
      this.r = Fe(e.r), this.g = Fe(e.g), this.b = Fe(e.b), this.a = typeof e.a == "number" ? Fe(e.a, 1) : 1;
    else if (t("hsl"))
      this.fromHsl(e);
    else if (t("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const t = this.toHsv();
    return t.h = e, this._c(t);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(o) {
      const s = o / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const t = e(this.r), r = e(this.g), i = e(this.b);
    return 0.2126 * t + 0.7152 * r + 0.0722 * i;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = ne(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
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
  darken(e = 10) {
    const t = this.getHue(), r = this.getSaturation();
    let i = this.getLightness() - e / 100;
    return i < 0 && (i = 0), this._c({
      h: t,
      s: r,
      l: i,
      a: this.a
    });
  }
  lighten(e = 10) {
    const t = this.getHue(), r = this.getSaturation();
    let i = this.getLightness() + e / 100;
    return i > 1 && (i = 1), this._c({
      h: t,
      s: r,
      l: i,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(e, t = 50) {
    const r = this._c(e), i = t / 100, o = (a) => (r[a] - this[a]) * i + this[a], s = {
      r: ne(o("r")),
      g: ne(o("g")),
      b: ne(o("b")),
      a: ne(o("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const t = this._c(e), r = this.a + t.a * (1 - this.a), i = (o) => ne((this[o] * this.a + t[o] * t.a * (1 - this.a)) / r);
    return this._c({
      r: i("r"),
      g: i("g"),
      b: i("b"),
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
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const t = (this.r || 0).toString(16);
    e += t.length === 2 ? t : "0" + t;
    const r = (this.g || 0).toString(16);
    e += r.length === 2 ? r : "0" + r;
    const i = (this.b || 0).toString(16);
    if (e += i.length === 2 ? i : "0" + i, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const o = ne(this.a * 255).toString(16);
      e += o.length === 2 ? o : "0" + o;
    }
    return e;
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
    const e = this.getHue(), t = ne(this.getSaturation() * 100), r = ne(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${t}%,${r}%,${this.a})` : `hsl(${e},${t}%,${r}%)`;
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
  _sc(e, t, r) {
    const i = this.clone();
    return i[e] = Fe(t, r), i;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const t = e.replace("#", "");
    function r(i, o) {
      return parseInt(t[i] + t[o || i], 16);
    }
    t.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = t[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = t[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: t,
    l: r,
    a: i
  }) {
    if (this._h = e % 360, this._s = t, this._l = r, this.a = typeof i == "number" ? i : 1, t <= 0) {
      const h = ne(r * 255);
      this.r = h, this.g = h, this.b = h;
    }
    let o = 0, s = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * r - 1)) * t, u = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (o = l, s = u) : c >= 1 && c < 2 ? (o = u, s = l) : c >= 2 && c < 3 ? (s = l, a = u) : c >= 3 && c < 4 ? (s = u, a = l) : c >= 4 && c < 5 ? (o = u, a = l) : c >= 5 && c < 6 && (o = l, a = u);
    const d = r - l / 2;
    this.r = ne((o + d) * 255), this.g = ne((s + d) * 255), this.b = ne((a + d) * 255);
  }
  fromHsv({
    h: e,
    s: t,
    v: r,
    a: i
  }) {
    this._h = e % 360, this._s = t, this._v = r, this.a = typeof i == "number" ? i : 1;
    const o = ne(r * 255);
    if (this.r = o, this.g = o, this.b = o, t <= 0)
      return;
    const s = e / 60, a = Math.floor(s), c = s - a, l = ne(r * (1 - t) * 255), u = ne(r * (1 - t * c) * 255), d = ne(r * (1 - t * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = d, this.b = l;
        break;
      case 1:
        this.r = u, this.b = l;
        break;
      case 2:
        this.r = l, this.b = d;
        break;
      case 3:
        this.r = l, this.g = u;
        break;
      case 4:
        this.r = d, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = u;
        break;
    }
  }
  fromHsvString(e) {
    const t = Ft(e, Vn);
    this.fromHsv({
      h: t[0],
      s: t[1],
      v: t[2],
      a: t[3]
    });
  }
  fromHslString(e) {
    const t = Ft(e, Vn);
    this.fromHsl({
      h: t[0],
      s: t[1],
      l: t[2],
      a: t[3]
    });
  }
  fromRgbString(e) {
    const t = Ft(e, (r, i) => (
      // Convert percentage to number. e.g. 50% -> 128
      i.includes("%") ? ne(r / 100 * 255) : r
    ));
    this.r = t[0], this.g = t[1], this.b = t[2], this.a = t[3];
  }
}
const $s = {
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
}, Is = Object.assign(Object.assign({}, $s), {
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
function Wt(n) {
  return n >= 0 && n <= 255;
}
function Je(n, e) {
  const {
    r: t,
    g: r,
    b: i,
    a: o
  } = new ye(n).toRgb();
  if (o < 1)
    return n;
  const {
    r: s,
    g: a,
    b: c
  } = new ye(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const u = Math.round((t - s * (1 - l)) / l), d = Math.round((r - a * (1 - l)) / l), h = Math.round((i - c * (1 - l)) / l);
    if (Wt(u) && Wt(d) && Wt(h))
      return new ye({
        r: u,
        g: d,
        b: h,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new ye({
    r: t,
    g: r,
    b: i,
    a: 1
  }).toRgbString();
}
var ks = function(n, e) {
  var t = {};
  for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && e.indexOf(r) < 0 && (t[r] = n[r]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, r = Object.getOwnPropertySymbols(n); i < r.length; i++)
    e.indexOf(r[i]) < 0 && Object.prototype.propertyIsEnumerable.call(n, r[i]) && (t[r[i]] = n[r[i]]);
  return t;
};
function Ds(n) {
  const {
    override: e
  } = n, t = ks(n, ["override"]), r = Object.assign({}, e);
  Object.keys(Is).forEach((h) => {
    delete r[h];
  });
  const i = Object.assign(Object.assign({}, t), r), o = 480, s = 576, a = 768, c = 992, l = 1200, u = 1600;
  if (i.motion === !1) {
    const h = "0s";
    i.motionDurationFast = h, i.motionDurationMid = h, i.motionDurationSlow = h;
  }
  return Object.assign(Object.assign(Object.assign({}, i), {
    // ============== Background ============== //
    colorFillContent: i.colorFillSecondary,
    colorFillContentHover: i.colorFill,
    colorFillAlter: i.colorFillQuaternary,
    colorBgContainerDisabled: i.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: i.colorBgContainer,
    colorSplit: Je(i.colorBorderSecondary, i.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: i.colorTextQuaternary,
    colorTextDisabled: i.colorTextQuaternary,
    colorTextHeading: i.colorText,
    colorTextLabel: i.colorTextSecondary,
    colorTextDescription: i.colorTextTertiary,
    colorTextLightSolid: i.colorWhite,
    colorHighlight: i.colorError,
    colorBgTextHover: i.colorFillSecondary,
    colorBgTextActive: i.colorFill,
    colorIcon: i.colorTextTertiary,
    colorIconHover: i.colorText,
    colorErrorOutline: Je(i.colorErrorBg, i.colorBgContainer),
    colorWarningOutline: Je(i.colorWarningBg, i.colorBgContainer),
    // Font
    fontSizeIcon: i.fontSizeSM,
    // Line
    lineWidthFocus: i.lineWidth * 3,
    // Control
    lineWidth: i.lineWidth,
    controlOutlineWidth: i.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: i.controlHeight / 2,
    controlItemBgHover: i.colorFillTertiary,
    controlItemBgActive: i.colorPrimaryBg,
    controlItemBgActiveHover: i.colorPrimaryBgHover,
    controlItemBgActiveDisabled: i.colorFill,
    controlTmpOutline: i.colorFillQuaternary,
    controlOutline: Je(i.colorPrimaryBg, i.colorBgContainer),
    lineType: i.lineType,
    borderRadius: i.borderRadius,
    borderRadiusXS: i.borderRadiusXS,
    borderRadiusSM: i.borderRadiusSM,
    borderRadiusLG: i.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: i.sizeXXS,
    paddingXS: i.sizeXS,
    paddingSM: i.sizeSM,
    padding: i.size,
    paddingMD: i.sizeMD,
    paddingLG: i.sizeLG,
    paddingXL: i.sizeXL,
    paddingContentHorizontalLG: i.sizeLG,
    paddingContentVerticalLG: i.sizeMS,
    paddingContentHorizontal: i.sizeMS,
    paddingContentVertical: i.sizeSM,
    paddingContentHorizontalSM: i.size,
    paddingContentVerticalSM: i.sizeXS,
    marginXXS: i.sizeXXS,
    marginXS: i.sizeXS,
    marginSM: i.sizeSM,
    margin: i.size,
    marginMD: i.sizeMD,
    marginLG: i.sizeLG,
    marginXL: i.sizeXL,
    marginXXL: i.sizeXXL,
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
    screenXS: o,
    screenXSMin: o,
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
    screenXLMax: u - 1,
    screenXXL: u,
    screenXXLMin: u,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ye("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ye("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ye("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const Ns = {
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
}, Fs = {
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
}, Ws = Di(ze.defaultAlgorithm), js = {
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
}, kr = (n, e, t) => {
  const r = t.getDerivativeToken(n), {
    override: i,
    ...o
  } = e;
  let s = {
    ...r,
    override: i
  };
  return s = Ds(s), o && Object.entries(o).forEach(([a, c]) => {
    const {
      theme: l,
      ...u
    } = c;
    let d = u;
    l && (d = kr({
      ...s,
      ...u
    }, {
      override: u
    }, l)), s[a] = d;
  }), s;
};
function Bs() {
  const {
    token: n,
    hashed: e,
    theme: t = Ws,
    override: r,
    cssVar: i
  } = f.useContext(ze._internalContext), [o, s, a] = Ni(t, [ze.defaultSeed, n], {
    salt: `${Mo}-${e || ""}`,
    override: r,
    getComputedToken: kr,
    cssVar: i && {
      prefix: i.prefix,
      key: i.key,
      unitless: Ns,
      ignore: Fs,
      preserve: js
    }
  });
  return [t, a, e ? s : "", o, i];
}
const {
  genStyleHooks: Dr
} = As({
  usePrefix: () => {
    const {
      getPrefixCls: n,
      iconPrefixCls: e
    } = Ve();
    return {
      iconPrefixCls: e,
      rootPrefixCls: n()
    };
  },
  useToken: () => {
    const [n, e, t, r, i] = Bs();
    return {
      theme: n,
      realToken: e,
      hashId: t,
      token: r,
      cssVar: i
    };
  },
  useCSP: () => {
    const {
      csp: n
    } = Ve();
    return n ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Hs = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-list-card`, i = t(n.fontSize).mul(n.lineHeight).mul(2).add(n.paddingSM).add(n.paddingSM).equal();
  return {
    [r]: {
      borderRadius: n.borderRadius,
      position: "relative",
      background: n.colorFillContent,
      borderWidth: n.lineWidth,
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
        padding: t(n.paddingSM).sub(n.lineWidth).equal(),
        paddingInlineStart: t(n.padding).add(n.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: n.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: t(n.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: t(n.paddingXXS).mul(1.5).equal(),
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
          color: n.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: i,
        height: i,
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
          background: `rgba(0, 0, 0, ${n.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: t(n.borderRadius).sub(n.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: n.paddingXXS
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
        padding: n.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: n.fontSize,
        cursor: "pointer",
        opacity: n.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: n.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: n.colorError,
        [`${r}-desc`]: {
          color: n.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((o) => `${o} ${n.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: t(n.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, rn = {
  "&, *": {
    boxSizing: "border-box"
  }
}, zs = (n) => {
  const {
    componentCls: e,
    calc: t,
    antCls: r
  } = n, i = `${e}-drop-area`, o = `${e}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [i]: {
      position: "absolute",
      inset: 0,
      zIndex: n.zIndexPopupBase,
      ...rn,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${o}-inner`]: {
          display: "none"
        }
      },
      [o]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [o]: {
        height: "100%",
        borderRadius: n.borderRadius,
        borderWidth: n.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: n.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: n.colorBgPlaceholderHover,
        ...rn,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${o}-drag-in`]: {
          borderColor: n.colorPrimaryHover
        },
        [`&${o}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${o}-inner`]: {
          gap: t(n.paddingXXS).div(2).equal()
        },
        [`${o}-icon`]: {
          fontSize: n.fontSizeHeading2,
          lineHeight: 1
        },
        [`${o}-title${o}-title`]: {
          margin: 0,
          fontSize: n.fontSize,
          lineHeight: n.lineHeight
        },
        [`${o}-description`]: {}
      }
    }
  };
}, Vs = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-list`, i = t(n.fontSize).mul(n.lineHeight).mul(2).add(n.paddingSM).add(n.paddingSM).equal();
  return {
    [e]: {
      position: "relative",
      width: "100%",
      ...rn,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: n.paddingSM,
        fontSize: n.fontSize,
        lineHeight: n.lineHeight,
        color: n.colorText,
        paddingBlock: n.paddingSM,
        paddingInline: n.padding,
        width: "100%",
        background: n.colorBgContainer,
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
            transition: `opacity ${n.motionDurationSlow}`,
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
          maxHeight: t(i).mul(3).equal(),
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
          width: i,
          height: i,
          fontSize: n.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: n.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: n.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: n.padding
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
}, Us = (n) => {
  const {
    colorBgContainer: e
  } = n;
  return {
    colorBgPlaceholderHover: new ye(e).setA(0.85).toRgbString()
  };
}, Nr = Dr("Attachments", (n) => {
  const e = Tt(n, {});
  return [zs(e), Vs(e), Hs(e)];
}, Us), Xs = (n) => n.indexOf("image/") === 0, et = 200;
function Gs(n) {
  return new Promise((e) => {
    if (!n || !n.type || !Xs(n.type)) {
      e("");
      return;
    }
    const t = new Image();
    if (t.onload = () => {
      const {
        width: r,
        height: i
      } = t, o = r / i, s = o > 1 ? et : et * o, a = o > 1 ? et / o : et, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(t, 0, 0, s, a);
      const u = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(t.src), e(u);
    }, t.crossOrigin = "anonymous", n.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (t.src = r.result);
      }, r.readAsDataURL(n);
    } else if (n.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && e(r.result);
      }, r.readAsDataURL(n);
    } else
      t.src = window.URL.createObjectURL(n);
  });
}
function qs() {
  return /* @__PURE__ */ f.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ f.createElement("title", null, "audio"), /* @__PURE__ */ f.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ f.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function Ks(n) {
  const {
    percent: e
  } = n, {
    token: t
  } = ze.useToken();
  return /* @__PURE__ */ f.createElement(Li, {
    type: "circle",
    percent: e,
    size: t.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ f.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function Ys() {
  return /* @__PURE__ */ f.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ f.createElement("title", null, "video"), /* @__PURE__ */ f.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ f.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const jt = " ", on = "#8c8c8c", Fr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Zs = [{
  icon: /* @__PURE__ */ f.createElement(fi, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ f.createElement(hi, null),
  color: on,
  ext: Fr
}, {
  icon: /* @__PURE__ */ f.createElement(pi, null),
  color: on,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ f.createElement(mi, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ f.createElement(gi, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ f.createElement(vi, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ f.createElement(bi, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ f.createElement(Ys, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ f.createElement(qs, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Un(n, e) {
  return e.some((t) => n.toLowerCase() === `.${t}`);
}
function Qs(n) {
  let e = n;
  const t = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; e >= 1024 && r < t.length - 1; )
    e /= 1024, r++;
  return `${e.toFixed(0)} ${t[r]}`;
}
function Js(n, e) {
  const {
    prefixCls: t,
    item: r,
    onRemove: i,
    className: o,
    style: s,
    imageProps: a
  } = n, c = f.useContext(Xe), {
    disabled: l
  } = c || {}, {
    name: u,
    size: d,
    percent: h,
    status: p = "done",
    description: b
  } = r, {
    getPrefixCls: v
  } = Ve(), g = v("attachment", t), m = `${g}-list-card`, [x, _, y] = Nr(g), [C, S] = f.useMemo(() => {
    const M = u || "", z = M.match(/^(.*)\.[^.]+$/);
    return z ? [z[1], M.slice(z[1].length)] : [M, ""];
  }, [u]), T = f.useMemo(() => Un(S, Fr), [S]), E = f.useMemo(() => b || (p === "uploading" ? `${h || 0}%` : p === "error" ? r.response || jt : d ? Qs(d) : jt), [p, h]), [P, $] = f.useMemo(() => {
    for (const {
      ext: M,
      icon: z,
      color: w
    } of Zs)
      if (Un(S, M))
        return [z, w];
    return [/* @__PURE__ */ f.createElement(ui, {
      key: "defaultIcon"
    }), on];
  }, [S]), [k, D] = f.useState();
  f.useEffect(() => {
    if (r.originFileObj) {
      let M = !0;
      return Gs(r.originFileObj).then((z) => {
        M && D(z);
      }), () => {
        M = !1;
      };
    }
    D(void 0);
  }, [r.originFileObj]);
  let N = null;
  const F = r.thumbUrl || r.url || k, L = T && (r.originFileObj || F);
  return L ? N = /* @__PURE__ */ f.createElement(f.Fragment, null, F && /* @__PURE__ */ f.createElement(Oi, ge({}, a, {
    alt: "preview",
    src: F
  })), p !== "done" && /* @__PURE__ */ f.createElement("div", {
    className: `${m}-img-mask`
  }, p === "uploading" && h !== void 0 && /* @__PURE__ */ f.createElement(Ks, {
    percent: h,
    prefixCls: m
  }), p === "error" && /* @__PURE__ */ f.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, E)))) : N = /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-icon`,
    style: {
      color: $
    }
  }, P), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-content`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-name`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, C ?? jt), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-suffix`
  }, S)), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, E)))), x(/* @__PURE__ */ f.createElement("div", {
    className: J(m, {
      [`${m}-status-${p}`]: p,
      [`${m}-type-preview`]: L,
      [`${m}-type-overview`]: !L
    }, o, _, y),
    style: s,
    ref: e
  }, N, !l && i && /* @__PURE__ */ f.createElement("button", {
    type: "button",
    className: `${m}-remove`,
    onClick: () => {
      i(r);
    }
  }, /* @__PURE__ */ f.createElement(di, null))));
}
const Wr = /* @__PURE__ */ f.forwardRef(Js), Xn = 1;
function ea(n) {
  const {
    prefixCls: e,
    items: t,
    onRemove: r,
    overflow: i,
    upload: o,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: l,
    imageProps: u
  } = n, d = `${e}-list`, h = f.useRef(null), [p, b] = f.useState(!1), {
    disabled: v
  } = f.useContext(Xe);
  f.useEffect(() => (b(!0), () => {
    b(!1);
  }), []);
  const [g, m] = f.useState(!1), [x, _] = f.useState(!1), y = () => {
    const E = h.current;
    E && (i === "scrollX" ? (m(Math.abs(E.scrollLeft) >= Xn), _(E.scrollWidth - E.clientWidth - Math.abs(E.scrollLeft) >= Xn)) : i === "scrollY" && (m(E.scrollTop !== 0), _(E.scrollHeight - E.clientHeight !== E.scrollTop)));
  };
  f.useEffect(() => {
    y();
  }, [i, t.length]);
  const C = (E) => {
    const P = h.current;
    P && P.scrollTo({
      left: P.scrollLeft + E * P.clientWidth,
      behavior: "smooth"
    });
  }, S = () => {
    C(-1);
  }, T = () => {
    C(1);
  };
  return /* @__PURE__ */ f.createElement("div", {
    className: J(d, {
      [`${d}-overflow-${n.overflow}`]: i,
      [`${d}-overflow-ping-start`]: g,
      [`${d}-overflow-ping-end`]: x
    }, s),
    ref: h,
    onScroll: y,
    style: a
  }, /* @__PURE__ */ f.createElement(ys, {
    keys: t.map((E) => ({
      key: E.uid,
      item: E
    })),
    motionName: `${d}-card-motion`,
    component: !1,
    motionAppear: p,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: E,
    item: P,
    className: $,
    style: k
  }) => /* @__PURE__ */ f.createElement(Wr, {
    key: E,
    prefixCls: e,
    item: P,
    onRemove: r,
    className: J($, c),
    imageProps: u,
    style: {
      ...k,
      ...l
    }
  })), !v && /* @__PURE__ */ f.createElement(Or, {
    upload: o
  }, /* @__PURE__ */ f.createElement(Ae, {
    className: `${d}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ f.createElement(yi, {
    className: `${d}-upload-btn-icon`
  }))), i === "scrollX" && /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(Ae, {
    size: "small",
    shape: "circle",
    className: `${d}-prev-btn`,
    icon: /* @__PURE__ */ f.createElement(wi, null),
    onClick: S
  }), /* @__PURE__ */ f.createElement(Ae, {
    size: "small",
    shape: "circle",
    className: `${d}-next-btn`,
    icon: /* @__PURE__ */ f.createElement(Si, null),
    onClick: T
  })));
}
function ta(n, e) {
  const {
    prefixCls: t,
    placeholder: r = {},
    upload: i,
    className: o,
    style: s
  } = n, a = `${t}-placeholder`, c = r || {}, {
    disabled: l
  } = f.useContext(Xe), [u, d] = f.useState(!1), h = () => {
    d(!0);
  }, p = (g) => {
    g.currentTarget.contains(g.relatedTarget) || d(!1);
  }, b = () => {
    d(!1);
  }, v = /* @__PURE__ */ f.isValidElement(r) ? r : /* @__PURE__ */ f.createElement(or, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ f.createElement(Lt.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ f.createElement(Lt.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ f.createElement(Lt.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ f.createElement("div", {
    className: J(a, {
      [`${a}-drag-in`]: u,
      [`${a}-disabled`]: l
    }, o),
    onDragEnter: h,
    onDragLeave: p,
    onDrop: b,
    "aria-hidden": l,
    style: s
  }, /* @__PURE__ */ f.createElement(ir.Dragger, ge({
    showUploadList: !1
  }, i, {
    ref: e,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), v));
}
const na = /* @__PURE__ */ f.forwardRef(ta);
function ra(n, e) {
  const {
    prefixCls: t,
    rootClassName: r,
    rootStyle: i,
    className: o,
    style: s,
    items: a,
    children: c,
    getDropContainer: l,
    placeholder: u,
    onChange: d,
    onRemove: h,
    overflow: p,
    imageProps: b,
    disabled: v,
    classNames: g = {},
    styles: m = {},
    ...x
  } = n, {
    getPrefixCls: _,
    direction: y
  } = Ve(), C = _("attachment", t), S = fr("attachments"), {
    classNames: T,
    styles: E
  } = S, P = f.useRef(null), $ = f.useRef(null);
  f.useImperativeHandle(e, () => ({
    nativeElement: P.current,
    upload: (W) => {
      var X, ee;
      const Z = (ee = (X = $.current) == null ? void 0 : X.nativeElement) == null ? void 0 : ee.querySelector('input[type="file"]');
      if (Z) {
        const re = new DataTransfer();
        re.items.add(W), Z.files = re.files, Z.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [k, D, N] = Nr(C), F = J(D, N), [L, M] = an([], {
    value: a
  }), z = Ee((W) => {
    M(W.fileList), d == null || d(W);
  }), w = {
    ...x,
    fileList: L,
    onChange: z
  }, fe = (W) => Promise.resolve(typeof h == "function" ? h(W) : h).then((Z) => {
    if (Z === !1)
      return;
    const X = L.filter((ee) => ee.uid !== W.uid);
    z({
      file: {
        ...W,
        status: "removed"
      },
      fileList: X
    });
  });
  let he;
  const V = (W, Z, X) => {
    const ee = typeof u == "function" ? u(W) : u;
    return /* @__PURE__ */ f.createElement(na, {
      placeholder: ee,
      upload: w,
      prefixCls: C,
      className: J(T.placeholder, g.placeholder),
      style: {
        ...E.placeholder,
        ...m.placeholder,
        ...Z == null ? void 0 : Z.style
      },
      ref: X
    });
  };
  if (c)
    he = /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(Or, {
      upload: w,
      rootClassName: r,
      ref: $
    }, c), /* @__PURE__ */ f.createElement(Mn, {
      getDropContainer: l,
      prefixCls: C,
      className: J(F, r)
    }, V("drop")));
  else {
    const W = L.length > 0;
    he = /* @__PURE__ */ f.createElement("div", {
      className: J(C, F, {
        [`${C}-rtl`]: y === "rtl"
      }, o, r),
      style: {
        ...i,
        ...s
      },
      dir: y || "ltr",
      ref: P
    }, /* @__PURE__ */ f.createElement(ea, {
      prefixCls: C,
      items: L,
      onRemove: fe,
      overflow: p,
      upload: w,
      listClassName: J(T.list, g.list),
      listStyle: {
        ...E.list,
        ...m.list,
        ...!W && {
          display: "none"
        }
      },
      itemClassName: J(T.item, g.item),
      itemStyle: {
        ...E.item,
        ...m.item
      },
      imageProps: b
    }), V("inline", W ? {
      style: {
        display: "none"
      }
    } : {}, $), /* @__PURE__ */ f.createElement(Mn, {
      getDropContainer: l || (() => P.current),
      prefixCls: C,
      className: F
    }, V("drop")));
  }
  return k(/* @__PURE__ */ f.createElement(Xe.Provider, {
    value: {
      disabled: v
    }
  }, he));
}
const jr = /* @__PURE__ */ f.forwardRef(ra);
jr.FileCard = Wr;
var ia = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, oa = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, sa = "".concat(ia, " ").concat(oa).split(/[\s\n]+/), aa = "aria-", la = "data-";
function Gn(n, e) {
  return n.indexOf(e) === 0;
}
function ca(n) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, t;
  e === !1 ? t = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? t = {
    aria: !0
  } : t = A({}, e);
  var r = {};
  return Object.keys(n).forEach(function(i) {
    // Aria
    (t.aria && (i === "role" || Gn(i, aa)) || // Data
    t.data && Gn(i, la) || // Attr
    t.attr && sa.includes(i)) && (r[i] = n[i]);
  }), r;
}
function ua(n, e) {
  return Zr(n, () => {
    const t = e(), {
      nativeElement: r
    } = t;
    return new Proxy(r, {
      get(i, o) {
        return t[o] ? t[o] : Reflect.get(i, o);
      }
    });
  });
}
const Br = /* @__PURE__ */ R.createContext({}), qn = () => ({
  height: 0
}), Kn = (n) => ({
  height: n.scrollHeight
});
function da(n) {
  const {
    title: e,
    onOpenChange: t,
    open: r,
    children: i,
    className: o,
    style: s,
    classNames: a = {},
    styles: c = {},
    closable: l,
    forceRender: u
  } = n, {
    prefixCls: d
  } = R.useContext(Br), h = `${d}-header`;
  return /* @__PURE__ */ R.createElement(Lr, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${h}-motion`,
    leavedClassName: `${h}-motion-hidden`,
    onEnterStart: qn,
    onEnterActive: Kn,
    onLeaveStart: Kn,
    onLeaveActive: qn,
    visible: r,
    forceRender: u
  }, ({
    className: p,
    style: b
  }) => /* @__PURE__ */ R.createElement("div", {
    className: J(h, p, o),
    style: {
      ...b,
      ...s
    }
  }, (l !== !1 || e) && /* @__PURE__ */ R.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      J(`${h}-header`, a.header)
    ),
    style: {
      ...c.header
    }
  }, /* @__PURE__ */ R.createElement("div", {
    className: `${h}-title`
  }, e), l !== !1 && /* @__PURE__ */ R.createElement("div", {
    className: `${h}-close`
  }, /* @__PURE__ */ R.createElement(Ae, {
    type: "text",
    icon: /* @__PURE__ */ R.createElement(xi, null),
    size: "small",
    onClick: () => {
      t == null || t(!r);
    }
  }))), i && /* @__PURE__ */ R.createElement("div", {
    className: J(`${h}-content`, a.content),
    style: {
      ...c.content
    }
  }, i)));
}
const Pt = /* @__PURE__ */ R.createContext(null);
function fa(n, e) {
  const {
    className: t,
    action: r,
    onClick: i,
    ...o
  } = n, s = R.useContext(Pt), {
    prefixCls: a,
    disabled: c
  } = s, l = s[r], u = c ?? o.disabled ?? s[`${r}Disabled`];
  return /* @__PURE__ */ R.createElement(Ae, ge({
    type: "text"
  }, o, {
    ref: e,
    onClick: (d) => {
      u || (l && l(), i && i(d));
    },
    className: J(a, t, {
      [`${a}-disabled`]: u
    })
  }));
}
const Mt = /* @__PURE__ */ R.forwardRef(fa);
function ha(n, e) {
  return /* @__PURE__ */ R.createElement(Mt, ge({
    icon: /* @__PURE__ */ R.createElement(Ci, null)
  }, n, {
    action: "onClear",
    ref: e
  }));
}
const pa = /* @__PURE__ */ R.forwardRef(ha), ma = /* @__PURE__ */ Qr((n) => {
  const {
    className: e
  } = n;
  return /* @__PURE__ */ f.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    className: e
  }, /* @__PURE__ */ f.createElement("title", null, "Stop Loading"), /* @__PURE__ */ f.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ f.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ f.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ f.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function ga(n, e) {
  const {
    prefixCls: t
  } = R.useContext(Pt), {
    className: r
  } = n;
  return /* @__PURE__ */ R.createElement(Mt, ge({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, n, {
    className: J(r, `${t}-loading-button`),
    action: "onCancel",
    ref: e
  }), /* @__PURE__ */ R.createElement(ma, {
    className: `${t}-loading-icon`
  }));
}
const Hr = /* @__PURE__ */ R.forwardRef(ga);
function va(n, e) {
  return /* @__PURE__ */ R.createElement(Mt, ge({
    icon: /* @__PURE__ */ R.createElement(Ei, null),
    type: "primary",
    shape: "circle"
  }, n, {
    action: "onSend",
    ref: e
  }));
}
const zr = /* @__PURE__ */ R.forwardRef(va), We = 1e3, je = 4, at = 140, Yn = at / 2, tt = 250, Zn = 500, nt = 0.8;
function ba({
  className: n
}) {
  return /* @__PURE__ */ f.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${We} ${We}`,
    xmlns: "http://www.w3.org/2000/svg",
    className: n
  }, /* @__PURE__ */ f.createElement("title", null, "Speech Recording"), Array.from({
    length: je
  }).map((e, t) => {
    const r = (We - at * je) / (je - 1), i = t * (r + at), o = We / 2 - tt / 2, s = We / 2 - Zn / 2;
    return /* @__PURE__ */ f.createElement("rect", {
      fill: "currentColor",
      rx: Yn,
      ry: Yn,
      height: tt,
      width: at,
      x: i,
      y: o,
      key: t
    }, /* @__PURE__ */ f.createElement("animate", {
      attributeName: "height",
      values: `${tt}; ${Zn}; ${tt}`,
      keyTimes: "0; 0.5; 1",
      dur: `${nt}s`,
      begin: `${nt / je * t}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ f.createElement("animate", {
      attributeName: "y",
      values: `${o}; ${s}; ${o}`,
      keyTimes: "0; 0.5; 1",
      dur: `${nt}s`,
      begin: `${nt / je * t}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function ya(n, e) {
  const {
    speechRecording: t,
    onSpeechDisabled: r,
    prefixCls: i
  } = R.useContext(Pt);
  let o = null;
  return t ? o = /* @__PURE__ */ R.createElement(ba, {
    className: `${i}-recording-icon`
  }) : r ? o = /* @__PURE__ */ R.createElement(_i, null) : o = /* @__PURE__ */ R.createElement(Ri, null), /* @__PURE__ */ R.createElement(Mt, ge({
    icon: o,
    color: "primary",
    variant: "text"
  }, n, {
    action: "onSpeech",
    ref: e
  }));
}
const Vr = /* @__PURE__ */ R.forwardRef(ya), wa = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-header`;
  return {
    [e]: {
      [r]: {
        borderBottomWidth: n.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: n.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: n.colorFillAlter,
          fontSize: n.fontSize,
          lineHeight: n.lineHeight,
          paddingBlock: t(n.paddingSM).sub(n.lineWidthBold).equal(),
          paddingInlineStart: n.padding,
          paddingInlineEnd: n.paddingXS,
          display: "flex",
          [`${r}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: n.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((i) => `${i} ${n.motionDurationSlow}`).join(","),
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
}, Sa = (n) => {
  const {
    componentCls: e,
    padding: t,
    paddingSM: r,
    paddingXS: i,
    paddingXXS: o,
    lineWidth: s,
    lineWidthBold: a,
    calc: c
  } = n;
  return {
    [e]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${n.boxShadowTertiary}`,
      transition: `background ${n.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: c(n.borderRadius).mul(2).equal()
      },
      borderColor: n.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${n.motionDurationSlow}`,
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
        boxShadow: `${n.boxShadowSecondary}`,
        borderColor: n.colorPrimary,
        "&:after": {
          borderWidth: a
        }
      },
      "&-disabled": {
        background: n.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${e}-content`]: {
        display: "flex",
        gap: i,
        width: "100%",
        paddingBlock: r,
        paddingInlineStart: t,
        paddingInlineEnd: r,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${e}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${e}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${e}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: n.paddingXS
        }
      },
      [`${e}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: n.controlHeight,
          width: n.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      },
      // ============================ Footer =============================
      [`${e}-footer`]: {
        paddingInlineStart: t,
        paddingInlineEnd: r,
        paddingBlockEnd: r,
        paddingBlockStart: o,
        boxSizing: "border-box"
      }
    }
  };
}, xa = () => ({}), Ca = Dr("Sender", (n) => {
  const {
    paddingXS: e,
    calc: t
  } = n, r = Tt(n, {
    SenderContentMaxWidth: `calc(100% - ${Xt(t(e).add(32).equal())})`
  });
  return [Sa(r), wa(r)];
}, xa);
let ft;
!ft && typeof window < "u" && (ft = window.SpeechRecognition || window.webkitSpeechRecognition);
function Ea(n, e) {
  const t = Ee(n), [r, i, o] = f.useMemo(() => typeof e == "object" ? [e.recording, e.onRecordingChange, typeof e.recording == "boolean"] : [void 0, void 0, !1], [e]), [s, a] = f.useState(null);
  f.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let v = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((g) => {
        a(g.state), g.onchange = function() {
          a(this.state);
        }, v = g;
      }), () => {
        v && (v.onchange = null);
      };
    }
  }, []);
  const c = ft && s !== "denied", l = f.useRef(null), [u, d] = an(!1, {
    value: r
  }), h = f.useRef(!1), p = () => {
    if (c && !l.current) {
      const v = new ft();
      v.onstart = () => {
        d(!0);
      }, v.onend = () => {
        d(!1);
      }, v.onresult = (g) => {
        var m, x, _;
        if (!h.current) {
          const y = (_ = (x = (m = g.results) == null ? void 0 : m[0]) == null ? void 0 : x[0]) == null ? void 0 : _.transcript;
          t(y);
        }
        h.current = !1;
      }, l.current = v;
    }
  }, b = Ee((v) => {
    v && !u || (h.current = v, o ? i == null || i(!u) : (p(), l.current && (u ? (l.current.stop(), i == null || i(!1)) : (l.current.start(), i == null || i(!0)))));
  });
  return [c, b, u];
}
function _a(n, e, t) {
  return Go(n, e) || t;
}
const Qn = {
  SendButton: zr,
  ClearButton: pa,
  LoadingButton: Hr,
  SpeechButton: Vr
}, Ra = /* @__PURE__ */ f.forwardRef((n, e) => {
  const {
    prefixCls: t,
    styles: r = {},
    classNames: i = {},
    className: o,
    rootClassName: s,
    style: a,
    defaultValue: c,
    value: l,
    readOnly: u,
    submitType: d = "enter",
    onSubmit: h,
    loading: p,
    components: b,
    onCancel: v,
    onChange: g,
    actions: m,
    onKeyPress: x,
    onKeyDown: _,
    disabled: y,
    allowSpeech: C,
    prefix: S,
    footer: T,
    header: E,
    onPaste: P,
    onPasteFile: $,
    autoSize: k = {
      maxRows: 8
    },
    ...D
  } = n, {
    direction: N,
    getPrefixCls: F
  } = Ve(), L = F("sender", t), M = f.useRef(null), z = f.useRef(null);
  ua(e, () => {
    var q, le;
    return {
      nativeElement: M.current,
      focus: (q = z.current) == null ? void 0 : q.focus,
      blur: (le = z.current) == null ? void 0 : le.blur
    };
  });
  const w = fr("sender"), fe = `${L}-input`, [he, V, W] = Ca(L), Z = J(L, w.className, o, s, V, W, {
    [`${L}-rtl`]: N === "rtl",
    [`${L}-disabled`]: y
  }), X = `${L}-actions-btn`, ee = `${L}-actions-list`, [re, j] = an(c || "", {
    value: l
  }), O = (q, le) => {
    j(q), g && g(q, le);
  }, [H, ie, G] = Ea((q) => {
    O(`${re} ${q}`);
  }, C), U = _a(b, ["input"], Ai.TextArea), pe = {
    ...ca(D, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: z
  }, K = () => {
    re && h && !p && h(re);
  }, ue = () => {
    O("");
  }, xe = f.useRef(!1), Q = () => {
    xe.current = !0;
  }, _e = () => {
    xe.current = !1;
  }, De = (q) => {
    const le = q.key === "Enter" && !xe.current;
    switch (d) {
      case "enter":
        le && !q.shiftKey && (q.preventDefault(), K());
        break;
      case "shiftEnter":
        le && q.shiftKey && (q.preventDefault(), K());
        break;
    }
    x && x(q);
  }, se = (q) => {
    var Ne;
    const le = (Ne = q.clipboardData) == null ? void 0 : Ne.files;
    le != null && le.length && $ && ($(le[0], le), q.preventDefault()), P == null || P(q);
  }, te = (q) => {
    var le, Ne;
    q.target !== ((le = M.current) == null ? void 0 : le.querySelector(`.${fe}`)) && q.preventDefault(), (Ne = z.current) == null || Ne.focus();
  };
  let ae = /* @__PURE__ */ f.createElement(or, {
    className: `${ee}-presets`
  }, C && /* @__PURE__ */ f.createElement(Vr, null), p ? /* @__PURE__ */ f.createElement(Hr, null) : /* @__PURE__ */ f.createElement(zr, null));
  typeof m == "function" ? ae = m(ae, {
    components: Qn
  }) : (m || m === !1) && (ae = m);
  const Te = {
    prefixCls: X,
    onSend: K,
    onSendDisabled: !re,
    onClear: ue,
    onClearDisabled: !re,
    onCancel: v,
    onCancelDisabled: !p,
    onSpeech: () => ie(!1),
    onSpeechDisabled: !H,
    speechRecording: G,
    disabled: y
  };
  let we = null;
  return typeof T == "function" ? we = T({
    components: Qn
  }) : T && (we = T), he(/* @__PURE__ */ f.createElement("div", {
    ref: M,
    className: Z,
    style: {
      ...w.style,
      ...a
    }
  }, E && /* @__PURE__ */ f.createElement(Br.Provider, {
    value: {
      prefixCls: L
    }
  }, E), /* @__PURE__ */ f.createElement(Pt.Provider, {
    value: Te
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${L}-content`,
    onMouseDown: te
  }, S && /* @__PURE__ */ f.createElement("div", {
    className: J(`${L}-prefix`, w.classNames.prefix, i.prefix),
    style: {
      ...w.styles.prefix,
      ...r.prefix
    }
  }, S), /* @__PURE__ */ f.createElement(U, ge({}, pe, {
    disabled: y,
    style: {
      ...w.styles.input,
      ...r.input
    },
    className: J(fe, w.classNames.input, i.input),
    autoSize: k,
    value: re,
    onChange: (q) => {
      O(q.target.value, q), ie(!0);
    },
    onPressEnter: De,
    onCompositionStart: Q,
    onCompositionEnd: _e,
    onKeyDown: _,
    onPaste: se,
    variant: "borderless",
    readOnly: u
  })), ae && /* @__PURE__ */ f.createElement("div", {
    className: J(ee, w.classNames.actions, i.actions),
    style: {
      ...w.styles.actions,
      ...r.actions
    }
  }, ae)), we && /* @__PURE__ */ f.createElement("div", {
    className: J(`${L}-footer`, w.classNames.footer, i.footer),
    style: {
      ...w.styles.footer,
      ...r.footer
    }
  }, we))));
}), sn = Ra;
sn.Header = da;
function Ta(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Pa(n, e = !1) {
  try {
    if (ii(n))
      return n;
    if (e && !Ta(n))
      return;
    if (typeof n == "string") {
      let t = n.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Jn(n, e) {
  return Vt(() => Pa(n, e), [n, e]);
}
function lt(n) {
  const e = de(n);
  return e.current = n, Jr((...t) => {
    var r;
    return (r = e.current) == null ? void 0 : r.call(e, ...t);
  }, []);
}
function Ma({
  value: n,
  onValueChange: e
}) {
  const [t, r] = He(n), i = de(e);
  i.current = e;
  const o = de(t);
  return o.current = t, Se(() => {
    i.current(t);
  }, [t]), Se(() => {
    Zi(n, o.current) || r(n);
  }, [n]), [t, r];
}
function La(n, e) {
  return Object.keys(n).reduce((t, r) => (n[r] !== void 0 && n[r] !== null && (t[r] = n[r]), t), {});
}
const Oa = ({
  children: n,
  ...e
}) => /* @__PURE__ */ Y.jsx(Y.Fragment, {
  children: n(e)
});
function Aa(n) {
  return f.createElement(Oa, {
    children: n
  });
}
function er(n, e) {
  return n ? e != null && e.forceClone || e != null && e.params ? Aa((t) => /* @__PURE__ */ Y.jsx(li, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ Y.jsx(Kt, {
      slot: n,
      clone: e == null ? void 0 : e.clone,
      ...t
    })
  })) : /* @__PURE__ */ Y.jsx(Kt, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function tr({
  key: n,
  slots: e,
  targets: t
}, r) {
  return e[n] ? (...i) => t ? t.map((o, s) => /* @__PURE__ */ Y.jsx(f.Fragment, {
    children: er(o, {
      clone: !0,
      params: i,
      forceClone: (r == null ? void 0 : r.forceClone) ?? !0
    })
  }, s)) : /* @__PURE__ */ Y.jsx(Y.Fragment, {
    children: er(e[n], {
      clone: !0,
      params: i,
      forceClone: (r == null ? void 0 : r.forceClone) ?? !0
    })
  }) : void 0;
}
function Bt(n, e, t, r) {
  return new (t || (t = Promise))(function(i, o) {
    function s(l) {
      try {
        c(r.next(l));
      } catch (u) {
        o(u);
      }
    }
    function a(l) {
      try {
        c(r.throw(l));
      } catch (u) {
        o(u);
      }
    }
    function c(l) {
      var u;
      l.done ? i(l.value) : (u = l.value, u instanceof t ? u : new t(function(d) {
        d(u);
      })).then(s, a);
    }
    c((r = r.apply(n, [])).next());
  });
}
class Ur {
  constructor() {
    this.listeners = {};
  }
  on(e, t, r) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), r == null ? void 0 : r.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  un(e, t) {
    var r;
    (r = this.listeners[e]) === null || r === void 0 || r.delete(t);
  }
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  unAll() {
    this.listeners = {};
  }
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((r) => r(...t));
  }
}
class $a extends Ur {
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  onInit() {
  }
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
class Ia extends Ur {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
const ka = ["audio/webm", "audio/wav", "audio/mpeg", "audio/mp4", "audio/mp3"];
class fn extends $a {
  constructor(e) {
    var t, r, i, o, s, a;
    super(Object.assign(Object.assign({}, e), {
      audioBitsPerSecond: (t = e.audioBitsPerSecond) !== null && t !== void 0 ? t : 128e3,
      scrollingWaveform: (r = e.scrollingWaveform) !== null && r !== void 0 && r,
      scrollingWaveformWindow: (i = e.scrollingWaveformWindow) !== null && i !== void 0 ? i : 5,
      continuousWaveform: (o = e.continuousWaveform) !== null && o !== void 0 && o,
      renderRecordedAudio: (s = e.renderRecordedAudio) === null || s === void 0 || s,
      mediaRecorderTimeslice: (a = e.mediaRecorderTimeslice) !== null && a !== void 0 ? a : void 0
    })), this.stream = null, this.mediaRecorder = null, this.dataWindow = null, this.isWaveformPaused = !1, this.lastStartTime = 0, this.lastDuration = 0, this.duration = 0, this.timer = new Ia(), this.subscriptions.push(this.timer.on("tick", () => {
      const c = performance.now() - this.lastStartTime;
      this.duration = this.isPaused() ? this.duration : this.lastDuration + c, this.emit("record-progress", this.duration);
    }));
  }
  static create(e) {
    return new fn(e || {});
  }
  renderMicStream(e) {
    var t;
    const r = new AudioContext(), i = r.createMediaStreamSource(e), o = r.createAnalyser();
    i.connect(o), this.options.continuousWaveform && (o.fftSize = 32);
    const s = o.frequencyBinCount, a = new Float32Array(s);
    let c = 0;
    this.wavesurfer && ((t = this.originalOptions) !== null && t !== void 0 || (this.originalOptions = Object.assign({}, this.wavesurfer.options)), this.wavesurfer.options.interact = !1, this.options.scrollingWaveform && (this.wavesurfer.options.cursorWidth = 0));
    const l = setInterval(() => {
      var u, d, h, p;
      if (!this.isWaveformPaused) {
        if (o.getFloatTimeDomainData(a), this.options.scrollingWaveform) {
          const b = Math.floor((this.options.scrollingWaveformWindow || 0) * r.sampleRate), v = Math.min(b, this.dataWindow ? this.dataWindow.length + s : s), g = new Float32Array(b);
          if (this.dataWindow) {
            const m = Math.max(0, b - this.dataWindow.length);
            g.set(this.dataWindow.slice(-v + s), m);
          }
          g.set(a, b - s), this.dataWindow = g;
        } else if (this.options.continuousWaveform) {
          if (!this.dataWindow) {
            const v = this.options.continuousWaveformDuration ? Math.round(100 * this.options.continuousWaveformDuration) : ((d = (u = this.wavesurfer) === null || u === void 0 ? void 0 : u.getWidth()) !== null && d !== void 0 ? d : 0) * window.devicePixelRatio;
            this.dataWindow = new Float32Array(v);
          }
          let b = 0;
          for (let v = 0; v < s; v++) {
            const g = Math.abs(a[v]);
            g > b && (b = g);
          }
          if (c + 1 > this.dataWindow.length) {
            const v = new Float32Array(2 * this.dataWindow.length);
            v.set(this.dataWindow, 0), this.dataWindow = v;
          }
          this.dataWindow[c] = b, c++;
        } else this.dataWindow = a;
        if (this.wavesurfer) {
          const b = ((p = (h = this.dataWindow) === null || h === void 0 ? void 0 : h.length) !== null && p !== void 0 ? p : 0) / 100;
          this.wavesurfer.load("", [this.dataWindow], this.options.scrollingWaveform ? this.options.scrollingWaveformWindow : b).then(() => {
            this.wavesurfer && this.options.continuousWaveform && (this.wavesurfer.setTime(this.getDuration() / 1e3), this.wavesurfer.options.minPxPerSec || this.wavesurfer.setOptions({
              minPxPerSec: this.wavesurfer.getWidth() / this.wavesurfer.getDuration()
            }));
          }).catch((v) => {
            console.error("Error rendering real-time recording data:", v);
          });
        }
      }
    }, 10);
    return {
      onDestroy: () => {
        clearInterval(l), i == null || i.disconnect(), r == null || r.close();
      },
      onEnd: () => {
        this.isWaveformPaused = !0, clearInterval(l), this.stopMic();
      }
    };
  }
  startMic(e) {
    return Bt(this, void 0, void 0, function* () {
      let t;
      try {
        t = yield navigator.mediaDevices.getUserMedia({
          audio: !(e != null && e.deviceId) || {
            deviceId: e.deviceId
          }
        });
      } catch (o) {
        throw new Error("Error accessing the microphone: " + o.message);
      }
      const {
        onDestroy: r,
        onEnd: i
      } = this.renderMicStream(t);
      return this.subscriptions.push(this.once("destroy", r)), this.subscriptions.push(this.once("record-end", i)), this.stream = t, t;
    });
  }
  stopMic() {
    this.stream && (this.stream.getTracks().forEach((e) => e.stop()), this.stream = null, this.mediaRecorder = null);
  }
  startRecording(e) {
    return Bt(this, void 0, void 0, function* () {
      const t = this.stream || (yield this.startMic(e));
      this.dataWindow = null;
      const r = this.mediaRecorder || new MediaRecorder(t, {
        mimeType: this.options.mimeType || ka.find((s) => MediaRecorder.isTypeSupported(s)),
        audioBitsPerSecond: this.options.audioBitsPerSecond
      });
      this.mediaRecorder = r, this.stopRecording();
      const i = [];
      r.ondataavailable = (s) => {
        s.data.size > 0 && i.push(s.data), this.emit("record-data-available", s.data);
      };
      const o = (s) => {
        var a;
        const c = new Blob(i, {
          type: r.mimeType
        });
        this.emit(s, c), this.options.renderRecordedAudio && (this.applyOriginalOptionsIfNeeded(), (a = this.wavesurfer) === null || a === void 0 || a.load(URL.createObjectURL(c)));
      };
      r.onpause = () => o("record-pause"), r.onstop = () => o("record-end"), r.start(this.options.mediaRecorderTimeslice), this.lastStartTime = performance.now(), this.lastDuration = 0, this.duration = 0, this.isWaveformPaused = !1, this.timer.start(), this.emit("record-start");
    });
  }
  getDuration() {
    return this.duration;
  }
  isRecording() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "recording";
  }
  isPaused() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "paused";
  }
  isActive() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) !== "inactive";
  }
  stopRecording() {
    var e;
    this.isActive() && ((e = this.mediaRecorder) === null || e === void 0 || e.stop(), this.timer.stop());
  }
  pauseRecording() {
    var e, t;
    this.isRecording() && (this.isWaveformPaused = !0, (e = this.mediaRecorder) === null || e === void 0 || e.requestData(), (t = this.mediaRecorder) === null || t === void 0 || t.pause(), this.timer.stop(), this.lastDuration = this.duration);
  }
  resumeRecording() {
    var e;
    this.isPaused() && (this.isWaveformPaused = !1, (e = this.mediaRecorder) === null || e === void 0 || e.resume(), this.timer.start(), this.lastStartTime = performance.now(), this.emit("record-resume"));
  }
  static getAvailableAudioDevices() {
    return Bt(this, void 0, void 0, function* () {
      return navigator.mediaDevices.enumerateDevices().then((e) => e.filter((t) => t.kind === "audioinput"));
    });
  }
  destroy() {
    this.applyOriginalOptionsIfNeeded(), super.destroy(), this.stopRecording(), this.stopMic();
  }
  applyOriginalOptionsIfNeeded() {
    this.wavesurfer && this.originalOptions && (this.wavesurfer.setOptions(this.originalOptions), delete this.originalOptions);
  }
}
class Ge {
  constructor() {
    this.listeners = {};
  }
  /** Subscribe to an event. Returns an unsubscribe function. */
  on(e, t, r) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), r != null && r.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  /** Unsubscribe from an event */
  un(e, t) {
    var r;
    (r = this.listeners[e]) === null || r === void 0 || r.delete(t);
  }
  /** Subscribe to an event only once */
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  /** Clear all events */
  unAll() {
    this.listeners = {};
  }
  /** Emit an event */
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((r) => r(...t));
  }
}
class Da extends Ge {
  /** Create a plugin instance */
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  /** Called after this.wavesurfer is available */
  onInit() {
  }
  /** Do not call directly, only called by WavesSurfer internally */
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  /** Destroy the plugin and unsubscribe from all events */
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
var Na = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
function Fa(n, e) {
  return Na(this, void 0, void 0, function* () {
    const t = new AudioContext({
      sampleRate: e
    });
    return t.decodeAudioData(n).finally(() => t.close());
  });
}
function Wa(n) {
  const e = n[0];
  if (e.some((t) => t > 1 || t < -1)) {
    const t = e.length;
    let r = 0;
    for (let i = 0; i < t; i++) {
      const o = Math.abs(e[i]);
      o > r && (r = o);
    }
    for (const i of n)
      for (let o = 0; o < t; o++)
        i[o] /= r;
  }
  return n;
}
function ja(n, e) {
  return typeof n[0] == "number" && (n = [n]), Wa(n), {
    duration: e,
    length: n[0].length,
    sampleRate: n[0].length / e,
    numberOfChannels: n.length,
    getChannelData: (t) => n == null ? void 0 : n[t],
    copyFromChannel: AudioBuffer.prototype.copyFromChannel,
    copyToChannel: AudioBuffer.prototype.copyToChannel
  };
}
const rt = {
  decode: Fa,
  createBuffer: ja
};
function Xr(n, e) {
  const t = e.xmlns ? document.createElementNS(e.xmlns, n) : document.createElement(n);
  for (const [r, i] of Object.entries(e))
    if (r === "children")
      for (const [o, s] of Object.entries(e))
        typeof s == "string" ? t.appendChild(document.createTextNode(s)) : t.appendChild(Xr(o, s));
    else r === "style" ? Object.assign(t.style, i) : r === "textContent" ? t.textContent = i : t.setAttribute(r, i.toString());
  return t;
}
function nr(n, e, t) {
  const r = Xr(n, e || {});
  return t == null || t.appendChild(r), r;
}
const Ba = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  createElement: nr,
  default: nr
}, Symbol.toStringTag, {
  value: "Module"
}));
var ct = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
function Ha(n, e) {
  return ct(this, void 0, void 0, function* () {
    if (!n.body || !n.headers) return;
    const t = n.body.getReader(), r = Number(n.headers.get("Content-Length")) || 0;
    let i = 0;
    const o = (a) => ct(this, void 0, void 0, function* () {
      i += (a == null ? void 0 : a.length) || 0;
      const c = Math.round(i / r * 100);
      e(c);
    }), s = () => ct(this, void 0, void 0, function* () {
      let a;
      try {
        a = yield t.read();
      } catch {
        return;
      }
      a.done || (o(a.value), yield s());
    });
    s();
  });
}
function za(n, e, t) {
  return ct(this, void 0, void 0, function* () {
    const r = yield fetch(n, t);
    if (r.status >= 400)
      throw new Error(`Failed to fetch ${n}: ${r.status} (${r.statusText})`);
    return Ha(r.clone(), e), r.blob();
  });
}
const Va = {
  fetchBlob: za
};
var Ua = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
class Xa extends Ge {
  constructor(e) {
    super(), this.isExternalMedia = !1, e.media ? (this.media = e.media, this.isExternalMedia = !0) : this.media = document.createElement("audio"), e.mediaControls && (this.media.controls = !0), e.autoplay && (this.media.autoplay = !0), e.playbackRate != null && this.onMediaEvent("canplay", () => {
      e.playbackRate != null && (this.media.playbackRate = e.playbackRate);
    }, {
      once: !0
    });
  }
  onMediaEvent(e, t, r) {
    return this.media.addEventListener(e, t, r), () => this.media.removeEventListener(e, t, r);
  }
  getSrc() {
    return this.media.currentSrc || this.media.src || "";
  }
  revokeSrc() {
    const e = this.getSrc();
    e.startsWith("blob:") && URL.revokeObjectURL(e);
  }
  canPlayType(e) {
    return this.media.canPlayType(e) !== "";
  }
  setSrc(e, t) {
    const r = this.getSrc();
    if (e && r === e) return;
    this.revokeSrc();
    const i = t instanceof Blob && (this.canPlayType(t.type) || !e) ? URL.createObjectURL(t) : e;
    r && (this.media.src = "");
    try {
      this.media.src = i;
    } catch {
      this.media.src = e;
    }
  }
  destroy() {
    this.isExternalMedia || (this.media.pause(), this.media.remove(), this.revokeSrc(), this.media.src = "", this.media.load());
  }
  setMediaElement(e) {
    this.media = e;
  }
  /** Start playing the audio */
  play() {
    return Ua(this, void 0, void 0, function* () {
      return this.media.play();
    });
  }
  /** Pause the audio */
  pause() {
    this.media.pause();
  }
  /** Check if the audio is playing */
  isPlaying() {
    return !this.media.paused && !this.media.ended;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.media.currentTime = Math.max(0, Math.min(e, this.getDuration()));
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    return this.media.duration;
  }
  /** Get the current audio position in seconds */
  getCurrentTime() {
    return this.media.currentTime;
  }
  /** Get the audio volume */
  getVolume() {
    return this.media.volume;
  }
  /** Set the audio volume */
  setVolume(e) {
    this.media.volume = e;
  }
  /** Get the audio muted state */
  getMuted() {
    return this.media.muted;
  }
  /** Mute or unmute the audio */
  setMuted(e) {
    this.media.muted = e;
  }
  /** Get the playback speed */
  getPlaybackRate() {
    return this.media.playbackRate;
  }
  /** Check if the audio is seeking */
  isSeeking() {
    return this.media.seeking;
  }
  /** Set the playback speed, pass an optional false to NOT preserve the pitch */
  setPlaybackRate(e, t) {
    t != null && (this.media.preservesPitch = t), this.media.playbackRate = e;
  }
  /** Get the HTML media element */
  getMediaElement() {
    return this.media;
  }
  /** Set a sink id to change the audio output device */
  setSinkId(e) {
    return this.media.setSinkId(e);
  }
}
function Ga(n, e, t, r, i = 3, o = 0, s = 100) {
  if (!n) return () => {
  };
  const a = matchMedia("(pointer: coarse)").matches;
  let c = () => {
  };
  const l = (u) => {
    if (u.button !== o) return;
    u.preventDefault(), u.stopPropagation();
    let d = u.clientX, h = u.clientY, p = !1;
    const b = Date.now(), v = (y) => {
      if (y.preventDefault(), y.stopPropagation(), a && Date.now() - b < s) return;
      const C = y.clientX, S = y.clientY, T = C - d, E = S - h;
      if (p || Math.abs(T) > i || Math.abs(E) > i) {
        const P = n.getBoundingClientRect(), {
          left: $,
          top: k
        } = P;
        p || (t == null || t(d - $, h - k), p = !0), e(T, E, C - $, S - k), d = C, h = S;
      }
    }, g = (y) => {
      if (p) {
        const C = y.clientX, S = y.clientY, T = n.getBoundingClientRect(), {
          left: E,
          top: P
        } = T;
        r == null || r(C - E, S - P);
      }
      c();
    }, m = (y) => {
      (!y.relatedTarget || y.relatedTarget === document.documentElement) && g(y);
    }, x = (y) => {
      p && (y.stopPropagation(), y.preventDefault());
    }, _ = (y) => {
      p && y.preventDefault();
    };
    document.addEventListener("pointermove", v), document.addEventListener("pointerup", g), document.addEventListener("pointerout", m), document.addEventListener("pointercancel", m), document.addEventListener("touchmove", _, {
      passive: !1
    }), document.addEventListener("click", x, {
      capture: !0
    }), c = () => {
      document.removeEventListener("pointermove", v), document.removeEventListener("pointerup", g), document.removeEventListener("pointerout", m), document.removeEventListener("pointercancel", m), document.removeEventListener("touchmove", _), setTimeout(() => {
        document.removeEventListener("click", x, {
          capture: !0
        });
      }, 10);
    };
  };
  return n.addEventListener("pointerdown", l), () => {
    c(), n.removeEventListener("pointerdown", l);
  };
}
var rr = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
}, qa = function(n, e) {
  var t = {};
  for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && e.indexOf(r) < 0 && (t[r] = n[r]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, r = Object.getOwnPropertySymbols(n); i < r.length; i++)
    e.indexOf(r[i]) < 0 && Object.prototype.propertyIsEnumerable.call(n, r[i]) && (t[r[i]] = n[r[i]]);
  return t;
};
class $e extends Ge {
  constructor(e, t) {
    super(), this.timeouts = [], this.isScrollable = !1, this.audioData = null, this.resizeObserver = null, this.lastContainerWidth = 0, this.isDragging = !1, this.subscriptions = [], this.unsubscribeOnScroll = [], this.subscriptions = [], this.options = e;
    const r = this.parentFromOptionsContainer(e.container);
    this.parent = r;
    const [i, o] = this.initHtml();
    r.appendChild(i), this.container = i, this.scrollContainer = o.querySelector(".scroll"), this.wrapper = o.querySelector(".wrapper"), this.canvasWrapper = o.querySelector(".canvases"), this.progressWrapper = o.querySelector(".progress"), this.cursor = o.querySelector(".cursor"), t && o.appendChild(t), this.initEvents();
  }
  parentFromOptionsContainer(e) {
    let t;
    if (typeof e == "string" ? t = document.querySelector(e) : e instanceof HTMLElement && (t = e), !t)
      throw new Error("Container not found");
    return t;
  }
  initEvents() {
    const e = (t) => {
      const r = this.wrapper.getBoundingClientRect(), i = t.clientX - r.left, o = t.clientY - r.top, s = i / r.width, a = o / r.height;
      return [s, a];
    };
    if (this.wrapper.addEventListener("click", (t) => {
      const [r, i] = e(t);
      this.emit("click", r, i);
    }), this.wrapper.addEventListener("dblclick", (t) => {
      const [r, i] = e(t);
      this.emit("dblclick", r, i);
    }), (this.options.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.scrollContainer.addEventListener("scroll", () => {
      const {
        scrollLeft: t,
        scrollWidth: r,
        clientWidth: i
      } = this.scrollContainer, o = t / r, s = (t + i) / r;
      this.emit("scroll", o, s, t, t + i);
    }), typeof ResizeObserver == "function") {
      const t = this.createDelay(100);
      this.resizeObserver = new ResizeObserver(() => {
        t().then(() => this.onContainerResize()).catch(() => {
        });
      }), this.resizeObserver.observe(this.scrollContainer);
    }
  }
  onContainerResize() {
    const e = this.parent.clientWidth;
    e === this.lastContainerWidth && this.options.height !== "auto" || (this.lastContainerWidth = e, this.reRender());
  }
  initDrag() {
    this.subscriptions.push(Ga(
      this.wrapper,
      // On drag
      (e, t, r) => {
        this.emit("drag", Math.max(0, Math.min(1, r / this.wrapper.getBoundingClientRect().width)));
      },
      // On start drag
      (e) => {
        this.isDragging = !0, this.emit("dragstart", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      },
      // On end drag
      (e) => {
        this.isDragging = !1, this.emit("dragend", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      }
    ));
  }
  getHeight(e, t) {
    var r;
    const o = ((r = this.audioData) === null || r === void 0 ? void 0 : r.numberOfChannels) || 1;
    if (e == null) return 128;
    if (!isNaN(Number(e))) return Number(e);
    if (e === "auto") {
      const s = this.parent.clientHeight || 128;
      return t != null && t.every((a) => !a.overlay) ? s / o : s;
    }
    return 128;
  }
  initHtml() {
    const e = document.createElement("div"), t = e.attachShadow({
      mode: "open"
    }), r = this.options.cspNonce && typeof this.options.cspNonce == "string" ? this.options.cspNonce.replace(/"/g, "") : "";
    return t.innerHTML = `
      <style${r ? ` nonce="${r}"` : ""}>
        :host {
          user-select: none;
          min-width: 1px;
        }
        :host audio {
          display: block;
          width: 100%;
        }
        :host .scroll {
          overflow-x: auto;
          overflow-y: hidden;
          width: 100%;
          position: relative;
        }
        :host .noScrollbar {
          scrollbar-color: transparent;
          scrollbar-width: none;
        }
        :host .noScrollbar::-webkit-scrollbar {
          display: none;
          -webkit-appearance: none;
        }
        :host .wrapper {
          position: relative;
          overflow: visible;
          z-index: 2;
        }
        :host .canvases {
          min-height: ${this.getHeight(this.options.height, this.options.splitChannels)}px;
        }
        :host .canvases > div {
          position: relative;
        }
        :host canvas {
          display: block;
          position: absolute;
          top: 0;
          image-rendering: pixelated;
        }
        :host .progress {
          pointer-events: none;
          position: absolute;
          z-index: 2;
          top: 0;
          left: 0;
          width: 0;
          height: 100%;
          overflow: hidden;
        }
        :host .progress > div {
          position: relative;
        }
        :host .cursor {
          pointer-events: none;
          position: absolute;
          z-index: 5;
          top: 0;
          left: 0;
          height: 100%;
          border-radius: 2px;
        }
      </style>

      <div class="scroll" part="scroll">
        <div class="wrapper" part="wrapper">
          <div class="canvases" part="canvases"></div>
          <div class="progress" part="progress"></div>
          <div class="cursor" part="cursor"></div>
        </div>
      </div>
    `, [e, t];
  }
  /** Wavesurfer itself calls this method. Do not call it manually. */
  setOptions(e) {
    if (this.options.container !== e.container) {
      const t = this.parentFromOptionsContainer(e.container);
      t.appendChild(this.container), this.parent = t;
    }
    (e.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.options = e, this.reRender();
  }
  getWrapper() {
    return this.wrapper;
  }
  getWidth() {
    return this.scrollContainer.clientWidth;
  }
  getScroll() {
    return this.scrollContainer.scrollLeft;
  }
  setScroll(e) {
    this.scrollContainer.scrollLeft = e;
  }
  setScrollPercentage(e) {
    const {
      scrollWidth: t
    } = this.scrollContainer, r = t * e;
    this.setScroll(r);
  }
  destroy() {
    var e, t;
    this.subscriptions.forEach((r) => r()), this.container.remove(), (e = this.resizeObserver) === null || e === void 0 || e.disconnect(), (t = this.unsubscribeOnScroll) === null || t === void 0 || t.forEach((r) => r()), this.unsubscribeOnScroll = [];
  }
  createDelay(e = 10) {
    let t, r;
    const i = () => {
      t && clearTimeout(t), r && r();
    };
    return this.timeouts.push(i), () => new Promise((o, s) => {
      i(), r = s, t = setTimeout(() => {
        t = void 0, r = void 0, o();
      }, e);
    });
  }
  // Convert array of color values to linear gradient
  convertColorValues(e) {
    if (!Array.isArray(e)) return e || "";
    if (e.length < 2) return e[0] || "";
    const t = document.createElement("canvas"), r = t.getContext("2d"), i = t.height * (window.devicePixelRatio || 1), o = r.createLinearGradient(0, 0, 0, i), s = 1 / (e.length - 1);
    return e.forEach((a, c) => {
      const l = c * s;
      o.addColorStop(l, a);
    }), o;
  }
  getPixelRatio() {
    return Math.max(1, window.devicePixelRatio || 1);
  }
  renderBarWaveform(e, t, r, i) {
    const o = e[0], s = e[1] || e[0], a = o.length, {
      width: c,
      height: l
    } = r.canvas, u = l / 2, d = this.getPixelRatio(), h = t.barWidth ? t.barWidth * d : 1, p = t.barGap ? t.barGap * d : t.barWidth ? h / 2 : 0, b = t.barRadius || 0, v = c / (h + p) / a, g = b && "roundRect" in r ? "roundRect" : "rect";
    r.beginPath();
    let m = 0, x = 0, _ = 0;
    for (let y = 0; y <= a; y++) {
      const C = Math.round(y * v);
      if (C > m) {
        const E = Math.round(x * u * i), P = Math.round(_ * u * i), $ = E + P || 1;
        let k = u - E;
        t.barAlign === "top" ? k = 0 : t.barAlign === "bottom" && (k = l - $), r[g](m * (h + p), k, h, $, b), m = C, x = 0, _ = 0;
      }
      const S = Math.abs(o[y] || 0), T = Math.abs(s[y] || 0);
      S > x && (x = S), T > _ && (_ = T);
    }
    r.fill(), r.closePath();
  }
  renderLineWaveform(e, t, r, i) {
    const o = (s) => {
      const a = e[s] || e[0], c = a.length, {
        height: l
      } = r.canvas, u = l / 2, d = r.canvas.width / c;
      r.moveTo(0, u);
      let h = 0, p = 0;
      for (let b = 0; b <= c; b++) {
        const v = Math.round(b * d);
        if (v > h) {
          const m = Math.round(p * u * i) || 1, x = u + m * (s === 0 ? -1 : 1);
          r.lineTo(h, x), h = v, p = 0;
        }
        const g = Math.abs(a[b] || 0);
        g > p && (p = g);
      }
      r.lineTo(h, u);
    };
    r.beginPath(), o(0), o(1), r.fill(), r.closePath();
  }
  renderWaveform(e, t, r) {
    if (r.fillStyle = this.convertColorValues(t.waveColor), t.renderFunction) {
      t.renderFunction(e, r);
      return;
    }
    let i = t.barHeight || 1;
    if (t.normalize) {
      const o = Array.from(e[0]).reduce((s, a) => Math.max(s, Math.abs(a)), 0);
      i = o ? 1 / o : 1;
    }
    if (t.barWidth || t.barGap || t.barAlign) {
      this.renderBarWaveform(e, t, r, i);
      return;
    }
    this.renderLineWaveform(e, t, r, i);
  }
  renderSingleCanvas(e, t, r, i, o, s, a) {
    const c = this.getPixelRatio(), l = document.createElement("canvas");
    l.width = Math.round(r * c), l.height = Math.round(i * c), l.style.width = `${r}px`, l.style.height = `${i}px`, l.style.left = `${Math.round(o)}px`, s.appendChild(l);
    const u = l.getContext("2d");
    if (this.renderWaveform(e, t, u), l.width > 0 && l.height > 0) {
      const d = l.cloneNode(), h = d.getContext("2d");
      h.drawImage(l, 0, 0), h.globalCompositeOperation = "source-in", h.fillStyle = this.convertColorValues(t.progressColor), h.fillRect(0, 0, l.width, l.height), a.appendChild(d);
    }
  }
  renderMultiCanvas(e, t, r, i, o, s) {
    const a = this.getPixelRatio(), {
      clientWidth: c
    } = this.scrollContainer, l = r / a;
    let u = Math.min($e.MAX_CANVAS_WIDTH, c, l), d = {};
    if (u === 0) return;
    if (t.barWidth || t.barGap) {
      const m = t.barWidth || 0.5, x = t.barGap || m / 2, _ = m + x;
      u % _ !== 0 && (u = Math.floor(u / _) * _);
    }
    const h = (m) => {
      if (m < 0 || m >= b || d[m]) return;
      d[m] = !0;
      const x = m * u, _ = Math.min(l - x, u);
      if (_ <= 0) return;
      const y = e.map((C) => {
        const S = Math.floor(x / l * C.length), T = Math.floor((x + _) / l * C.length);
        return C.slice(S, T);
      });
      this.renderSingleCanvas(y, t, _, i, x, o, s);
    }, p = () => {
      Object.keys(d).length > $e.MAX_NODES && (o.innerHTML = "", s.innerHTML = "", d = {});
    }, b = Math.ceil(l / u);
    if (!this.isScrollable) {
      for (let m = 0; m < b; m++)
        h(m);
      return;
    }
    const v = this.scrollContainer.scrollLeft / l, g = Math.floor(v * b);
    if (h(g - 1), h(g), h(g + 1), b > 1) {
      const m = this.on("scroll", () => {
        const {
          scrollLeft: x
        } = this.scrollContainer, _ = Math.floor(x / l * b);
        p(), h(_ - 1), h(_), h(_ + 1);
      });
      this.unsubscribeOnScroll.push(m);
    }
  }
  renderChannel(e, t, r, i) {
    var {
      overlay: o
    } = t, s = qa(t, ["overlay"]);
    const a = document.createElement("div"), c = this.getHeight(s.height, s.splitChannels);
    a.style.height = `${c}px`, o && i > 0 && (a.style.marginTop = `-${c}px`), this.canvasWrapper.style.minHeight = `${c}px`, this.canvasWrapper.appendChild(a);
    const l = a.cloneNode();
    this.progressWrapper.appendChild(l), this.renderMultiCanvas(e, s, r, c, a, l);
  }
  render(e) {
    return rr(this, void 0, void 0, function* () {
      var t;
      this.timeouts.forEach((c) => c()), this.timeouts = [], this.canvasWrapper.innerHTML = "", this.progressWrapper.innerHTML = "", this.options.width != null && (this.scrollContainer.style.width = typeof this.options.width == "number" ? `${this.options.width}px` : this.options.width);
      const r = this.getPixelRatio(), i = this.scrollContainer.clientWidth, o = Math.ceil(e.duration * (this.options.minPxPerSec || 0));
      this.isScrollable = o > i;
      const s = this.options.fillParent && !this.isScrollable, a = (s ? i : o) * r;
      if (this.wrapper.style.width = s ? "100%" : `${o}px`, this.scrollContainer.style.overflowX = this.isScrollable ? "auto" : "hidden", this.scrollContainer.classList.toggle("noScrollbar", !!this.options.hideScrollbar), this.cursor.style.backgroundColor = `${this.options.cursorColor || this.options.progressColor}`, this.cursor.style.width = `${this.options.cursorWidth}px`, this.audioData = e, this.emit("render"), this.options.splitChannels)
        for (let c = 0; c < e.numberOfChannels; c++) {
          const l = Object.assign(Object.assign({}, this.options), (t = this.options.splitChannels) === null || t === void 0 ? void 0 : t[c]);
          this.renderChannel([e.getChannelData(c)], l, a, c);
        }
      else {
        const c = [e.getChannelData(0)];
        e.numberOfChannels > 1 && c.push(e.getChannelData(1)), this.renderChannel(c, this.options, a, 0);
      }
      Promise.resolve().then(() => this.emit("rendered"));
    });
  }
  reRender() {
    if (this.unsubscribeOnScroll.forEach((r) => r()), this.unsubscribeOnScroll = [], !this.audioData) return;
    const {
      scrollWidth: e
    } = this.scrollContainer, {
      right: t
    } = this.progressWrapper.getBoundingClientRect();
    if (this.render(this.audioData), this.isScrollable && e !== this.scrollContainer.scrollWidth) {
      const {
        right: r
      } = this.progressWrapper.getBoundingClientRect();
      let i = r - t;
      i *= 2, i = i < 0 ? Math.floor(i) : Math.ceil(i), i /= 2, this.scrollContainer.scrollLeft += i;
    }
  }
  zoom(e) {
    this.options.minPxPerSec = e, this.reRender();
  }
  scrollIntoView(e, t = !1) {
    const {
      scrollLeft: r,
      scrollWidth: i,
      clientWidth: o
    } = this.scrollContainer, s = e * i, a = r, c = r + o, l = o / 2;
    if (this.isDragging)
      s + 30 > c ? this.scrollContainer.scrollLeft += 30 : s - 30 < a && (this.scrollContainer.scrollLeft -= 30);
    else {
      (s < a || s > c) && (this.scrollContainer.scrollLeft = s - (this.options.autoCenter ? l : 0));
      const u = s - r - l;
      t && this.options.autoCenter && u > 0 && (this.scrollContainer.scrollLeft += Math.min(u, 10));
    }
    {
      const u = this.scrollContainer.scrollLeft, d = u / i, h = (u + o) / i;
      this.emit("scroll", d, h, u, u + o);
    }
  }
  renderProgress(e, t) {
    if (isNaN(e)) return;
    const r = e * 100;
    this.canvasWrapper.style.clipPath = `polygon(${r}% 0, 100% 0, 100% 100%, ${r}% 100%)`, this.progressWrapper.style.width = `${r}%`, this.cursor.style.left = `${r}%`, this.cursor.style.transform = `translateX(-${Math.round(r) === 100 ? this.options.cursorWidth : 0}px)`, this.isScrollable && this.options.autoScroll && this.scrollIntoView(e, t);
  }
  exportImage(e, t, r) {
    return rr(this, void 0, void 0, function* () {
      const i = this.canvasWrapper.querySelectorAll("canvas");
      if (!i.length)
        throw new Error("No waveform data");
      if (r === "dataURL") {
        const o = Array.from(i).map((s) => s.toDataURL(e, t));
        return Promise.resolve(o);
      }
      return Promise.all(Array.from(i).map((o) => new Promise((s, a) => {
        o.toBlob((c) => {
          c ? s(c) : a(new Error("Could not export image"));
        }, e, t);
      })));
    });
  }
}
$e.MAX_CANVAS_WIDTH = 8e3;
$e.MAX_NODES = 10;
class Ka extends Ge {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
var Ht = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
class zt extends Ge {
  constructor(e = new AudioContext()) {
    super(), this.bufferNode = null, this.playStartTime = 0, this.playedDuration = 0, this._muted = !1, this._playbackRate = 1, this._duration = void 0, this.buffer = null, this.currentSrc = "", this.paused = !0, this.crossOrigin = null, this.seeking = !1, this.autoplay = !1, this.addEventListener = this.on, this.removeEventListener = this.un, this.audioContext = e, this.gainNode = this.audioContext.createGain(), this.gainNode.connect(this.audioContext.destination);
  }
  load() {
    return Ht(this, void 0, void 0, function* () {
    });
  }
  get src() {
    return this.currentSrc;
  }
  set src(e) {
    if (this.currentSrc = e, this._duration = void 0, !e) {
      this.buffer = null, this.emit("emptied");
      return;
    }
    fetch(e).then((t) => {
      if (t.status >= 400)
        throw new Error(`Failed to fetch ${e}: ${t.status} (${t.statusText})`);
      return t.arrayBuffer();
    }).then((t) => this.currentSrc !== e ? null : this.audioContext.decodeAudioData(t)).then((t) => {
      this.currentSrc === e && (this.buffer = t, this.emit("loadedmetadata"), this.emit("canplay"), this.autoplay && this.play());
    });
  }
  _play() {
    var e;
    if (!this.paused) return;
    this.paused = !1, (e = this.bufferNode) === null || e === void 0 || e.disconnect(), this.bufferNode = this.audioContext.createBufferSource(), this.buffer && (this.bufferNode.buffer = this.buffer), this.bufferNode.playbackRate.value = this._playbackRate, this.bufferNode.connect(this.gainNode);
    let t = this.playedDuration * this._playbackRate;
    (t >= this.duration || t < 0) && (t = 0, this.playedDuration = 0), this.bufferNode.start(this.audioContext.currentTime, t), this.playStartTime = this.audioContext.currentTime, this.bufferNode.onended = () => {
      this.currentTime >= this.duration && (this.pause(), this.emit("ended"));
    };
  }
  _pause() {
    var e;
    this.paused = !0, (e = this.bufferNode) === null || e === void 0 || e.stop(), this.playedDuration += this.audioContext.currentTime - this.playStartTime;
  }
  play() {
    return Ht(this, void 0, void 0, function* () {
      this.paused && (this._play(), this.emit("play"));
    });
  }
  pause() {
    this.paused || (this._pause(), this.emit("pause"));
  }
  stopAt(e) {
    const t = e - this.currentTime, r = this.bufferNode;
    r == null || r.stop(this.audioContext.currentTime + t), r == null || r.addEventListener("ended", () => {
      r === this.bufferNode && (this.bufferNode = null, this.pause());
    }, {
      once: !0
    });
  }
  setSinkId(e) {
    return Ht(this, void 0, void 0, function* () {
      return this.audioContext.setSinkId(e);
    });
  }
  get playbackRate() {
    return this._playbackRate;
  }
  set playbackRate(e) {
    this._playbackRate = e, this.bufferNode && (this.bufferNode.playbackRate.value = e);
  }
  get currentTime() {
    return (this.paused ? this.playedDuration : this.playedDuration + (this.audioContext.currentTime - this.playStartTime)) * this._playbackRate;
  }
  set currentTime(e) {
    const t = !this.paused;
    t && this._pause(), this.playedDuration = e / this._playbackRate, t && this._play(), this.emit("seeking"), this.emit("timeupdate");
  }
  get duration() {
    var e, t;
    return (e = this._duration) !== null && e !== void 0 ? e : ((t = this.buffer) === null || t === void 0 ? void 0 : t.duration) || 0;
  }
  set duration(e) {
    this._duration = e;
  }
  get volume() {
    return this.gainNode.gain.value;
  }
  set volume(e) {
    this.gainNode.gain.value = e, this.emit("volumechange");
  }
  get muted() {
    return this._muted;
  }
  set muted(e) {
    this._muted !== e && (this._muted = e, this._muted ? this.gainNode.disconnect() : this.gainNode.connect(this.audioContext.destination));
  }
  canPlayType(e) {
    return /^(audio|video)\//.test(e);
  }
  /** Get the GainNode used to play the audio. Can be used to attach filters. */
  getGainNode() {
    return this.gainNode;
  }
  /** Get decoded audio */
  getChannelData() {
    const e = [];
    if (!this.buffer) return e;
    const t = this.buffer.numberOfChannels;
    for (let r = 0; r < t; r++)
      e.push(this.buffer.getChannelData(r));
    return e;
  }
}
var Pe = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
const Ya = {
  waveColor: "#999",
  progressColor: "#555",
  cursorWidth: 1,
  minPxPerSec: 0,
  fillParent: !0,
  interact: !0,
  dragToSeek: !1,
  autoScroll: !0,
  autoCenter: !0,
  sampleRate: 8e3
};
class qe extends Xa {
  /** Create a new WaveSurfer instance */
  static create(e) {
    return new qe(e);
  }
  /** Create a new WaveSurfer instance */
  constructor(e) {
    const t = e.media || (e.backend === "WebAudio" ? new zt() : void 0);
    super({
      media: t,
      mediaControls: e.mediaControls,
      autoplay: e.autoplay,
      playbackRate: e.audioRate
    }), this.plugins = [], this.decodedData = null, this.stopAtPosition = null, this.subscriptions = [], this.mediaSubscriptions = [], this.abortController = null, this.options = Object.assign({}, Ya, e), this.timer = new Ka();
    const r = t ? void 0 : this.getMediaElement();
    this.renderer = new $e(this.options, r), this.initPlayerEvents(), this.initRendererEvents(), this.initTimerEvents(), this.initPlugins();
    const i = this.options.url || this.getSrc() || "";
    Promise.resolve().then(() => {
      this.emit("init");
      const {
        peaks: o,
        duration: s
      } = this.options;
      (i || o && s) && this.load(i, o, s).catch(() => null);
    });
  }
  updateProgress(e = this.getCurrentTime()) {
    return this.renderer.renderProgress(e / this.getDuration(), this.isPlaying()), e;
  }
  initTimerEvents() {
    this.subscriptions.push(this.timer.on("tick", () => {
      if (!this.isSeeking()) {
        const e = this.updateProgress();
        this.emit("timeupdate", e), this.emit("audioprocess", e), this.stopAtPosition != null && this.isPlaying() && e >= this.stopAtPosition && this.pause();
      }
    }));
  }
  initPlayerEvents() {
    this.isPlaying() && (this.emit("play"), this.timer.start()), this.mediaSubscriptions.push(this.onMediaEvent("timeupdate", () => {
      const e = this.updateProgress();
      this.emit("timeupdate", e);
    }), this.onMediaEvent("play", () => {
      this.emit("play"), this.timer.start();
    }), this.onMediaEvent("pause", () => {
      this.emit("pause"), this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("emptied", () => {
      this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("ended", () => {
      this.emit("timeupdate", this.getDuration()), this.emit("finish"), this.stopAtPosition = null;
    }), this.onMediaEvent("seeking", () => {
      this.emit("seeking", this.getCurrentTime());
    }), this.onMediaEvent("error", () => {
      var e;
      this.emit("error", (e = this.getMediaElement().error) !== null && e !== void 0 ? e : new Error("Media error")), this.stopAtPosition = null;
    }));
  }
  initRendererEvents() {
    this.subscriptions.push(
      // Seek on click
      this.renderer.on("click", (e, t) => {
        this.options.interact && (this.seekTo(e), this.emit("interaction", e * this.getDuration()), this.emit("click", e, t));
      }),
      // Double click
      this.renderer.on("dblclick", (e, t) => {
        this.emit("dblclick", e, t);
      }),
      // Scroll
      this.renderer.on("scroll", (e, t, r, i) => {
        const o = this.getDuration();
        this.emit("scroll", e * o, t * o, r, i);
      }),
      // Redraw
      this.renderer.on("render", () => {
        this.emit("redraw");
      }),
      // RedrawComplete
      this.renderer.on("rendered", () => {
        this.emit("redrawcomplete");
      }),
      // DragStart
      this.renderer.on("dragstart", (e) => {
        this.emit("dragstart", e);
      }),
      // DragEnd
      this.renderer.on("dragend", (e) => {
        this.emit("dragend", e);
      })
    );
    {
      let e;
      this.subscriptions.push(this.renderer.on("drag", (t) => {
        if (!this.options.interact) return;
        this.renderer.renderProgress(t), clearTimeout(e);
        let r;
        this.isPlaying() ? r = 0 : this.options.dragToSeek === !0 ? r = 200 : typeof this.options.dragToSeek == "object" && this.options.dragToSeek !== void 0 && (r = this.options.dragToSeek.debounceTime), e = setTimeout(() => {
          this.seekTo(t);
        }, r), this.emit("interaction", t * this.getDuration()), this.emit("drag", t);
      }));
    }
  }
  initPlugins() {
    var e;
    !((e = this.options.plugins) === null || e === void 0) && e.length && this.options.plugins.forEach((t) => {
      this.registerPlugin(t);
    });
  }
  unsubscribePlayerEvents() {
    this.mediaSubscriptions.forEach((e) => e()), this.mediaSubscriptions = [];
  }
  /** Set new wavesurfer options and re-render it */
  setOptions(e) {
    this.options = Object.assign({}, this.options, e), e.duration && !e.peaks && (this.decodedData = rt.createBuffer(this.exportPeaks(), e.duration)), e.peaks && e.duration && (this.decodedData = rt.createBuffer(e.peaks, e.duration)), this.renderer.setOptions(this.options), e.audioRate && this.setPlaybackRate(e.audioRate), e.mediaControls != null && (this.getMediaElement().controls = e.mediaControls);
  }
  /** Register a wavesurfer.js plugin */
  registerPlugin(e) {
    return e._init(this), this.plugins.push(e), this.subscriptions.push(e.once("destroy", () => {
      this.plugins = this.plugins.filter((t) => t !== e);
    })), e;
  }
  /** For plugins only: get the waveform wrapper div */
  getWrapper() {
    return this.renderer.getWrapper();
  }
  /** For plugins only: get the scroll container client width */
  getWidth() {
    return this.renderer.getWidth();
  }
  /** Get the current scroll position in pixels */
  getScroll() {
    return this.renderer.getScroll();
  }
  /** Set the current scroll position in pixels */
  setScroll(e) {
    return this.renderer.setScroll(e);
  }
  /** Move the start of the viewing window to a specific time in the audio (in seconds) */
  setScrollTime(e) {
    const t = e / this.getDuration();
    this.renderer.setScrollPercentage(t);
  }
  /** Get all registered plugins */
  getActivePlugins() {
    return this.plugins;
  }
  loadAudio(e, t, r, i) {
    return Pe(this, void 0, void 0, function* () {
      var o;
      if (this.emit("load", e), !this.options.media && this.isPlaying() && this.pause(), this.decodedData = null, this.stopAtPosition = null, !t && !r) {
        const a = this.options.fetchParams || {};
        window.AbortController && !a.signal && (this.abortController = new AbortController(), a.signal = (o = this.abortController) === null || o === void 0 ? void 0 : o.signal);
        const c = (u) => this.emit("loading", u);
        t = yield Va.fetchBlob(e, c, a);
        const l = this.options.blobMimeType;
        l && (t = new Blob([t], {
          type: l
        }));
      }
      this.setSrc(e, t);
      const s = yield new Promise((a) => {
        const c = i || this.getDuration();
        c ? a(c) : this.mediaSubscriptions.push(this.onMediaEvent("loadedmetadata", () => a(this.getDuration()), {
          once: !0
        }));
      });
      if (!e && !t) {
        const a = this.getMediaElement();
        a instanceof zt && (a.duration = s);
      }
      if (r)
        this.decodedData = rt.createBuffer(r, s || 0);
      else if (t) {
        const a = yield t.arrayBuffer();
        this.decodedData = yield rt.decode(a, this.options.sampleRate);
      }
      this.decodedData && (this.emit("decode", this.getDuration()), this.renderer.render(this.decodedData)), this.emit("ready", this.getDuration());
    });
  }
  /** Load an audio file by URL, with optional pre-decoded audio data */
  load(e, t, r) {
    return Pe(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio(e, void 0, t, r);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Load an audio blob */
  loadBlob(e, t, r) {
    return Pe(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio("", e, t, r);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Zoom the waveform by a given pixels-per-second factor */
  zoom(e) {
    if (!this.decodedData)
      throw new Error("No audio loaded");
    this.renderer.zoom(e), this.emit("zoom", e);
  }
  /** Get the decoded audio data */
  getDecodedData() {
    return this.decodedData;
  }
  /** Get decoded peaks */
  exportPeaks({
    channels: e = 2,
    maxLength: t = 8e3,
    precision: r = 1e4
  } = {}) {
    if (!this.decodedData)
      throw new Error("The audio has not been decoded yet");
    const i = Math.min(e, this.decodedData.numberOfChannels), o = [];
    for (let s = 0; s < i; s++) {
      const a = this.decodedData.getChannelData(s), c = [], l = a.length / t;
      for (let u = 0; u < t; u++) {
        const d = a.slice(Math.floor(u * l), Math.ceil((u + 1) * l));
        let h = 0;
        for (let p = 0; p < d.length; p++) {
          const b = d[p];
          Math.abs(b) > Math.abs(h) && (h = b);
        }
        c.push(Math.round(h * r) / r);
      }
      o.push(c);
    }
    return o;
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    let e = super.getDuration() || 0;
    return (e === 0 || e === 1 / 0) && this.decodedData && (e = this.decodedData.duration), e;
  }
  /** Toggle if the waveform should react to clicks */
  toggleInteraction(e) {
    this.options.interact = e;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.stopAtPosition = null, super.setTime(e), this.updateProgress(e), this.emit("timeupdate", e);
  }
  /** Seek to a percentage of audio as [0..1] (0 = beginning, 1 = end) */
  seekTo(e) {
    const t = this.getDuration() * e;
    this.setTime(t);
  }
  /** Start playing the audio */
  play(e, t) {
    const r = Object.create(null, {
      play: {
        get: () => super.play
      }
    });
    return Pe(this, void 0, void 0, function* () {
      e != null && this.setTime(e);
      const i = yield r.play.call(this);
      return t != null && (this.media instanceof zt ? this.media.stopAt(t) : this.stopAtPosition = t), i;
    });
  }
  /** Play or pause the audio */
  playPause() {
    return Pe(this, void 0, void 0, function* () {
      return this.isPlaying() ? this.pause() : this.play();
    });
  }
  /** Stop the audio and go to the beginning */
  stop() {
    this.pause(), this.setTime(0);
  }
  /** Skip N or -N seconds from the current position */
  skip(e) {
    this.setTime(this.getCurrentTime() + e);
  }
  /** Empty the waveform */
  empty() {
    this.load("", [[0]], 1e-3);
  }
  /** Set HTML media element */
  setMediaElement(e) {
    this.unsubscribePlayerEvents(), super.setMediaElement(e), this.initPlayerEvents();
  }
  exportImage() {
    return Pe(this, arguments, void 0, function* (e = "image/png", t = 1, r = "dataURL") {
      return this.renderer.exportImage(e, t, r);
    });
  }
  /** Unmount wavesurfer */
  destroy() {
    var e;
    this.emit("destroy"), (e = this.abortController) === null || e === void 0 || e.abort(), this.plugins.forEach((t) => t.destroy()), this.subscriptions.forEach((t) => t()), this.unsubscribePlayerEvents(), this.timer.destroy(), this.renderer.destroy(), super.destroy();
  }
}
qe.BasePlugin = Da;
qe.dom = Ba;
function Za({
  container: n,
  onStop: e
}) {
  const t = de(null), [r, i] = He(!1), o = lt(() => {
    var c;
    (c = t.current) == null || c.startRecording();
  }), s = lt(() => {
    var c;
    (c = t.current) == null || c.stopRecording();
  }), a = lt(e);
  return Se(() => {
    if (n) {
      const l = qe.create({
        normalize: !1,
        container: n
      }).registerPlugin(fn.create());
      t.current = l, l.on("record-start", () => {
        i(!0);
      }), l.on("record-end", (u) => {
        a(u), i(!1);
      });
    }
  }, [n, a]), {
    recording: r,
    start: o,
    stop: s
  };
}
function Qa(n) {
  const e = function(a, c, l) {
    for (let u = 0; u < l.length; u++)
      a.setUint8(c + u, l.charCodeAt(u));
  }, t = n.numberOfChannels, r = n.length * t * 2 + 44, i = new ArrayBuffer(r), o = new DataView(i);
  let s = 0;
  e(o, s, "RIFF"), s += 4, o.setUint32(s, r - 8, !0), s += 4, e(o, s, "WAVE"), s += 4, e(o, s, "fmt "), s += 4, o.setUint32(s, 16, !0), s += 4, o.setUint16(s, 1, !0), s += 2, o.setUint16(s, t, !0), s += 2, o.setUint32(s, n.sampleRate, !0), s += 4, o.setUint32(s, n.sampleRate * 2 * t, !0), s += 4, o.setUint16(s, t * 2, !0), s += 2, o.setUint16(s, 16, !0), s += 2, e(o, s, "data"), s += 4, o.setUint32(s, n.length * t * 2, !0), s += 4;
  for (let a = 0; a < n.numberOfChannels; a++) {
    const c = n.getChannelData(a);
    for (let l = 0; l < c.length; l++)
      o.setInt16(s, c[l] * 65535, !0), s += 2;
  }
  return new Uint8Array(i);
}
async function Ja(n, e, t) {
  const r = await n.arrayBuffer(), o = await new AudioContext().decodeAudioData(r), s = new AudioContext(), a = o.numberOfChannels, c = o.sampleRate;
  let l = o.length, u = 0;
  const d = s.createBuffer(a, l, c);
  for (let h = 0; h < a; h++) {
    const p = o.getChannelData(h), b = d.getChannelData(h);
    for (let v = 0; v < l; v++)
      b[v] = p[u + v];
  }
  return Promise.resolve(Qa(d));
}
const el = (n) => !!n.name, Be = (n) => {
  var e;
  return {
    text: (n == null ? void 0 : n.text) || "",
    files: ((e = n == null ? void 0 : n.files) == null ? void 0 : e.map((t) => t.path)) || []
  };
}, rl = Eo(({
  onValueChange: n,
  onChange: e,
  onPasteFile: t,
  onUpload: r,
  onSubmit: i,
  onRemove: o,
  onDownload: s,
  onDrop: a,
  onPreview: c,
  upload: l,
  onCancel: u,
  children: d,
  readOnly: h,
  loading: p,
  disabled: b,
  placeholder: v,
  elRef: g,
  slots: m,
  setSlotParams: x,
  uploadConfig: _,
  value: y,
  ...C
}) => {
  var ee, re;
  const [S, T] = He(!1), E = ci(), P = de(null), $ = Jn(C.actions, !0), k = Jn(C.footer, !0), {
    token: D
  } = ze.useToken(), {
    start: N,
    stop: F,
    recording: L
  } = Za({
    container: P.current,
    async onStop(j) {
      const O = new File([await Ja(j)], `${Date.now()}_recording_result.wav`, {
        type: "audio/wav"
      });
      he(O);
    }
  }), [M, z] = Ma({
    onValueChange: n,
    value: y
  }), w = Vt(() => oi(_), [_]), fe = b || (w == null ? void 0 : w.disabled) || p || h, he = lt(async (j) => {
    if (fe)
      return;
    V.current = !0;
    const O = w == null ? void 0 : w.maxCount;
    if (typeof O == "number" && O > 0 && W.length >= O)
      return;
    let H = Array.isArray(j) ? j : [j];
    if (O === 1)
      H = H.slice(0, 1);
    else if (H.length === 0) {
      V.current = !1;
      return;
    } else if (typeof O == "number") {
      const K = O - W.length;
      H = H.slice(0, K < 0 ? 0 : K);
    }
    const ie = W, G = H.map((K) => ({
      ...K,
      size: K.size,
      uid: `${K.name}-${Date.now()}`,
      name: K.name,
      status: "uploading"
    }));
    Z((K) => [...O === 1 ? [] : K, ...G]);
    const U = (await l(H)).filter(Boolean).map((K, ue) => ({
      ...K,
      uid: G[ue].uid
    })), me = O === 1 ? U : [...ie, ...U];
    r == null || r(U.map((K) => K.path)), V.current = !1;
    const pe = {
      ...M,
      files: me
    };
    return e == null || e(Be(pe)), z(pe), U;
  }), V = de(!1), [W, Z] = He(() => (M == null ? void 0 : M.files) || []);
  Se(() => {
    Z((M == null ? void 0 : M.files) || []);
  }, [M == null ? void 0 : M.files]);
  const X = Vt(() => {
    const j = {};
    return W.map((O) => {
      if (!el(O)) {
        const H = O.uid || O.url || O.path;
        return j[H] || (j[H] = 0), j[H]++, {
          ...O,
          name: O.orig_name || O.path,
          uid: O.uid || H + "-" + j[H],
          status: "done"
        };
      }
      return O;
    }) || [];
  }, [W]);
  return /* @__PURE__ */ Y.jsxs(Y.Fragment, {
    children: [/* @__PURE__ */ Y.jsx("div", {
      style: {
        display: "none"
      },
      ref: P
    }), /* @__PURE__ */ Y.jsx("div", {
      style: {
        display: "none"
      },
      children: d
    }), /* @__PURE__ */ Y.jsx(sn, {
      ...C,
      value: M == null ? void 0 : M.text,
      ref: g,
      disabled: b,
      readOnly: h,
      allowSpeech: w != null && w.allowSpeech ? {
        recording: L,
        onRecordingChange(j) {
          fe || (j ? N() : F());
        }
      } : !1,
      placeholder: v,
      loading: p,
      onSubmit: () => {
        E || i == null || i(Be(M));
      },
      onCancel: () => {
        u == null || u();
      },
      onChange: (j) => {
        const O = {
          ...M,
          text: j
        };
        e == null || e(Be(O)), z(O);
      },
      onPasteFile: async (j, O) => {
        if (!((w == null ? void 0 : w.allowPasteFile) ?? !0))
          return;
        const H = await he(Array.from(O));
        H && (t == null || t(H.map((ie) => ie.path)));
      },
      prefix: /* @__PURE__ */ Y.jsxs(Y.Fragment, {
        children: [(w == null ? void 0 : w.allowUpload) ?? !0 ? /* @__PURE__ */ Y.jsx($i, {
          title: w == null ? void 0 : w.uploadButtonTooltip,
          children: /* @__PURE__ */ Y.jsx(Ii, {
            count: ((w == null ? void 0 : w.showCount) ?? !0) && !S ? X.length : 0,
            children: /* @__PURE__ */ Y.jsx(Ae, {
              onClick: () => {
                T(!S);
              },
              color: "default",
              variant: "text",
              icon: /* @__PURE__ */ Y.jsx(Pi, {})
            })
          })
        }) : null, m.prefix ? /* @__PURE__ */ Y.jsx(Kt, {
          slot: m.prefix
        }) : null]
      }),
      actions: m.actions ? tr({
        slots: m,
        key: "actions"
      }, {}) : $ || C.actions,
      footer: m.footer ? tr({
        slots: m,
        key: "footer"
      }) : k || C.footer,
      header: /* @__PURE__ */ Y.jsx(sn.Header, {
        title: (w == null ? void 0 : w.title) || "Attachments",
        open: S,
        onOpenChange: T,
        children: /* @__PURE__ */ Y.jsx(jr, {
          ...La(si(w, ["title", "placeholder", "showCount", "buttonTooltip", "allowPasteFile"])),
          imageProps: {
            ...w == null ? void 0 : w.imageProps,
            wrapperStyle: {
              width: "100%",
              height: "100%",
              ...(ee = w == null ? void 0 : w.imageProps) == null ? void 0 : ee.wrapperStyle
            },
            style: {
              width: "100%",
              height: "100%",
              objectFit: "contain",
              borderRadius: D.borderRadius,
              ...(re = w == null ? void 0 : w.imageProps) == null ? void 0 : re.style
            }
          },
          disabled: fe,
          getDropContainer: () => w != null && w.fullscreenDrop ? document.body : null,
          items: X,
          placeholder: (j) => {
            var H, ie, G, U, me, pe;
            const O = j === "drop";
            return {
              title: O ? ((H = w == null ? void 0 : w.placeholder) == null ? void 0 : H.drop.title) ?? "Drop file here" : ((ie = w == null ? void 0 : w.placeholder) == null ? void 0 : ie.inline.title) ?? "Upload files",
              description: O ? ((G = w == null ? void 0 : w.placeholder) == null ? void 0 : G.drop.description) ?? void 0 : ((U = w == null ? void 0 : w.placeholder) == null ? void 0 : U.inline.description) ?? "Click or drag files to this area to upload",
              icon: O ? ((me = w == null ? void 0 : w.placeholder) == null ? void 0 : me.drop.icon) ?? void 0 : ((pe = w == null ? void 0 : w.placeholder) == null ? void 0 : pe.inline.icon) ?? /* @__PURE__ */ Y.jsx(Ti, {})
            };
          },
          onDownload: s,
          onPreview: c,
          onDrop: a,
          onChange: async (j) => {
            const O = j.file, H = j.fileList, ie = X.findIndex((G) => G.uid === O.uid);
            if (ie !== -1) {
              if (V.current)
                return;
              o == null || o(O);
              const G = W.slice();
              G.splice(ie, 1);
              const U = {
                ...M,
                files: G
              };
              z(U), e == null || e(Be(U));
            } else {
              if (V.current)
                return;
              V.current = !0;
              let G = H.filter((Q) => Q.status !== "done");
              const U = w == null ? void 0 : w.maxCount;
              if (U === 1)
                G = G.slice(0, 1);
              else if (G.length === 0) {
                V.current = !1;
                return;
              } else if (typeof U == "number") {
                const Q = U - W.length;
                G = G.slice(0, Q < 0 ? 0 : Q);
              }
              const me = W, pe = G.map((Q) => ({
                ...Q,
                size: Q.size,
                uid: Q.uid,
                name: Q.name,
                status: "uploading"
              }));
              Z((Q) => [...U === 1 ? [] : Q, ...pe]);
              const K = (await l(G.map((Q) => Q.originFileObj))).filter(Boolean).map((Q, _e) => ({
                ...Q,
                uid: pe[_e].uid
              })), ue = U === 1 ? K : [...me, ...K];
              r == null || r(K.map((Q) => Q.path)), V.current = !1;
              const xe = {
                ...M,
                files: ue
              };
              Z(ue), n == null || n(xe), e == null || e(Be(xe));
            }
          },
          customRequest: Xi
        })
      })
    })]
  });
});
export {
  rl as MultimodalInput,
  rl as default
};

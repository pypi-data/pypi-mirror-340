const {
  SvelteComponent: El,
  assign: kl,
  create_slot: Al,
  detach: yl,
  element: $l,
  get_all_dirty_from_scope: Ll,
  get_slot_changes: ql,
  get_spread_update: Rl,
  init: Ol,
  insert: Nl,
  safe_not_equal: Dl,
  set_dynamic_element_data: Yn,
  set_style: oe,
  toggle_class: Ee,
  transition_in: Yo,
  transition_out: jo,
  update_slot_base: Ml
} = window.__gradio__svelte__internal;
function Il(n) {
  let e, t, o;
  const l = (
    /*#slots*/
    n[18].default
  ), i = Al(
    l,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let s = 0; s < a.length; s += 1)
    r = kl(r, a[s]);
  return {
    c() {
      e = $l(
        /*tag*/
        n[14]
      ), i && i.c(), Yn(
        /*tag*/
        n[14]
      )(e, r), Ee(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), Ee(
        e,
        "padded",
        /*padding*/
        n[6]
      ), Ee(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), Ee(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), Ee(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), oe(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), oe(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), oe(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), oe(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), oe(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), oe(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), oe(e, "border-width", "var(--block-border-width)");
    },
    m(s, _) {
      Nl(s, e, _), i && i.m(e, null), o = !0;
    },
    p(s, _) {
      i && i.p && (!o || _ & /*$$scope*/
      131072) && Ml(
        i,
        l,
        s,
        /*$$scope*/
        s[17],
        o ? ql(
          l,
          /*$$scope*/
          s[17],
          _,
          null
        ) : Ll(
          /*$$scope*/
          s[17]
        ),
        null
      ), Yn(
        /*tag*/
        s[14]
      )(e, r = Rl(a, [
        (!o || _ & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!o || _ & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!o || _ & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Ee(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), Ee(
        e,
        "padded",
        /*padding*/
        s[6]
      ), Ee(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), Ee(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), Ee(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), _ & /*height*/
      1 && oe(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), _ & /*width*/
      2 && oe(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), _ & /*variant*/
      16 && oe(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), _ & /*allow_overflow*/
      2048 && oe(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && oe(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), _ & /*min_width*/
      8192 && oe(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      o || (Yo(i, s), o = !0);
    },
    o(s) {
      jo(i, s), o = !1;
    },
    d(s) {
      s && yl(e), i && i.d(s);
    }
  };
}
function Pl(n) {
  let e, t = (
    /*tag*/
    n[14] && Il(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(o, l) {
      t && t.m(o, l), e = !0;
    },
    p(o, [l]) {
      /*tag*/
      o[14] && t.p(o, l);
    },
    i(o) {
      e || (Yo(t, o), e = !0);
    },
    o(o) {
      jo(t, o), e = !1;
    },
    d(o) {
      t && t.d(o);
    }
  };
}
function Fl(n, e, t) {
  let { $$slots: o = {}, $$scope: l } = e, { height: i = void 0 } = e, { width: a = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: s = [] } = e, { variant: _ = "solid" } = e, { border_mode: c = "base" } = e, { padding: d = !0 } = e, { type: u = "normal" } = e, { test_id: g = void 0 } = e, { explicit_call: T = !1 } = e, { container: k = !0 } = e, { visible: y = !0 } = e, { allow_overflow: R = !0 } = e, { scale: h = null } = e, { min_width: m = 0 } = e, p = u === "fieldset" ? "fieldset" : "div";
  const $ = (S) => {
    if (S !== void 0) {
      if (typeof S == "number")
        return S + "px";
      if (typeof S == "string")
        return S;
    }
  };
  return n.$$set = (S) => {
    "height" in S && t(0, i = S.height), "width" in S && t(1, a = S.width), "elem_id" in S && t(2, r = S.elem_id), "elem_classes" in S && t(3, s = S.elem_classes), "variant" in S && t(4, _ = S.variant), "border_mode" in S && t(5, c = S.border_mode), "padding" in S && t(6, d = S.padding), "type" in S && t(16, u = S.type), "test_id" in S && t(7, g = S.test_id), "explicit_call" in S && t(8, T = S.explicit_call), "container" in S && t(9, k = S.container), "visible" in S && t(10, y = S.visible), "allow_overflow" in S && t(11, R = S.allow_overflow), "scale" in S && t(12, h = S.scale), "min_width" in S && t(13, m = S.min_width), "$$scope" in S && t(17, l = S.$$scope);
  }, [
    i,
    a,
    r,
    s,
    _,
    c,
    d,
    g,
    T,
    k,
    y,
    R,
    h,
    m,
    p,
    $,
    u,
    l,
    o
  ];
}
class Ul extends El {
  constructor(e) {
    super(), Ol(this, e, Fl, Pl, Dl, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: zl,
  attr: Hl,
  create_slot: Bl,
  detach: Gl,
  element: Wl,
  get_all_dirty_from_scope: Vl,
  get_slot_changes: Yl,
  init: jl,
  insert: Xl,
  safe_not_equal: Zl,
  transition_in: Kl,
  transition_out: Jl,
  update_slot_base: Ql
} = window.__gradio__svelte__internal;
function xl(n) {
  let e, t;
  const o = (
    /*#slots*/
    n[1].default
  ), l = Bl(
    o,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = Wl("div"), l && l.c(), Hl(e, "class", "svelte-1hnfib2");
    },
    m(i, a) {
      Xl(i, e, a), l && l.m(e, null), t = !0;
    },
    p(i, [a]) {
      l && l.p && (!t || a & /*$$scope*/
      1) && Ql(
        l,
        o,
        i,
        /*$$scope*/
        i[0],
        t ? Yl(
          o,
          /*$$scope*/
          i[0],
          a,
          null
        ) : Vl(
          /*$$scope*/
          i[0]
        ),
        null
      );
    },
    i(i) {
      t || (Kl(l, i), t = !0);
    },
    o(i) {
      Jl(l, i), t = !1;
    },
    d(i) {
      i && Gl(e), l && l.d(i);
    }
  };
}
function ei(n, e, t) {
  let { $$slots: o = {}, $$scope: l } = e;
  return n.$$set = (i) => {
    "$$scope" in i && t(0, l = i.$$scope);
  }, [l, o];
}
class ti extends zl {
  constructor(e) {
    super(), jl(this, e, ei, xl, Zl, {});
  }
}
const {
  SvelteComponent: ni,
  attr: jn,
  check_outros: oi,
  create_component: li,
  create_slot: ii,
  destroy_component: ai,
  detach: Ut,
  element: si,
  empty: ri,
  get_all_dirty_from_scope: _i,
  get_slot_changes: fi,
  group_outros: ci,
  init: ui,
  insert: zt,
  mount_component: di,
  safe_not_equal: mi,
  set_data: pi,
  space: gi,
  text: hi,
  toggle_class: nt,
  transition_in: Ct,
  transition_out: Ht,
  update_slot_base: bi
} = window.__gradio__svelte__internal;
function Xn(n) {
  let e, t;
  return e = new ti({
    props: {
      $$slots: { default: [wi] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      li(e.$$.fragment);
    },
    m(o, l) {
      di(e, o, l), t = !0;
    },
    p(o, l) {
      const i = {};
      l & /*$$scope, info*/
      10 && (i.$$scope = { dirty: l, ctx: o }), e.$set(i);
    },
    i(o) {
      t || (Ct(e.$$.fragment, o), t = !0);
    },
    o(o) {
      Ht(e.$$.fragment, o), t = !1;
    },
    d(o) {
      ai(e, o);
    }
  };
}
function wi(n) {
  let e;
  return {
    c() {
      e = hi(
        /*info*/
        n[1]
      );
    },
    m(t, o) {
      zt(t, e, o);
    },
    p(t, o) {
      o & /*info*/
      2 && pi(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Ut(e);
    }
  };
}
function vi(n) {
  let e, t, o, l;
  const i = (
    /*#slots*/
    n[2].default
  ), a = ii(
    i,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && Xn(n)
  );
  return {
    c() {
      e = si("span"), a && a.c(), t = gi(), r && r.c(), o = ri(), jn(e, "data-testid", "block-info"), jn(e, "class", "svelte-22c38v"), nt(e, "sr-only", !/*show_label*/
      n[0]), nt(e, "hide", !/*show_label*/
      n[0]), nt(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(s, _) {
      zt(s, e, _), a && a.m(e, null), zt(s, t, _), r && r.m(s, _), zt(s, o, _), l = !0;
    },
    p(s, [_]) {
      a && a.p && (!l || _ & /*$$scope*/
      8) && bi(
        a,
        i,
        s,
        /*$$scope*/
        s[3],
        l ? fi(
          i,
          /*$$scope*/
          s[3],
          _,
          null
        ) : _i(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!l || _ & /*show_label*/
      1) && nt(e, "sr-only", !/*show_label*/
      s[0]), (!l || _ & /*show_label*/
      1) && nt(e, "hide", !/*show_label*/
      s[0]), (!l || _ & /*info*/
      2) && nt(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? r ? (r.p(s, _), _ & /*info*/
      2 && Ct(r, 1)) : (r = Xn(s), r.c(), Ct(r, 1), r.m(o.parentNode, o)) : r && (ci(), Ht(r, 1, 1, () => {
        r = null;
      }), oi());
    },
    i(s) {
      l || (Ct(a, s), Ct(r), l = !0);
    },
    o(s) {
      Ht(a, s), Ht(r), l = !1;
    },
    d(s) {
      s && (Ut(e), Ut(t), Ut(o)), a && a.d(s), r && r.d(s);
    }
  };
}
function Si(n, e, t) {
  let { $$slots: o = {}, $$scope: l } = e, { show_label: i = !0 } = e, { info: a = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, i = r.show_label), "info" in r && t(1, a = r.info), "$$scope" in r && t(3, l = r.$$scope);
  }, [i, a, o, l];
}
class Ti extends ni {
  constructor(e) {
    super(), ui(this, e, Si, vi, mi, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: ir,
  append: ar,
  attr: sr,
  create_component: rr,
  destroy_component: _r,
  detach: fr,
  element: cr,
  init: ur,
  insert: dr,
  mount_component: mr,
  safe_not_equal: pr,
  set_data: gr,
  space: hr,
  text: br,
  toggle_class: wr,
  transition_in: vr,
  transition_out: Sr
} = window.__gradio__svelte__internal, {
  SvelteComponent: Ci,
  append: mn,
  attr: Oe,
  bubble: Ei,
  create_component: ki,
  destroy_component: Ai,
  detach: Xo,
  element: pn,
  init: yi,
  insert: Zo,
  listen: $i,
  mount_component: Li,
  safe_not_equal: qi,
  set_data: Ri,
  set_style: ot,
  space: Oi,
  text: Ni,
  toggle_class: te,
  transition_in: Di,
  transition_out: Mi
} = window.__gradio__svelte__internal;
function Zn(n) {
  let e, t;
  return {
    c() {
      e = pn("span"), t = Ni(
        /*label*/
        n[1]
      ), Oe(e, "class", "svelte-1lrphxw");
    },
    m(o, l) {
      Zo(o, e, l), mn(e, t);
    },
    p(o, l) {
      l & /*label*/
      2 && Ri(
        t,
        /*label*/
        o[1]
      );
    },
    d(o) {
      o && Xo(e);
    }
  };
}
function Ii(n) {
  let e, t, o, l, i, a, r, s = (
    /*show_label*/
    n[2] && Zn(n)
  );
  return l = new /*Icon*/
  n[0]({}), {
    c() {
      e = pn("button"), s && s.c(), t = Oi(), o = pn("div"), ki(l.$$.fragment), Oe(o, "class", "svelte-1lrphxw"), te(
        o,
        "small",
        /*size*/
        n[4] === "small"
      ), te(
        o,
        "large",
        /*size*/
        n[4] === "large"
      ), te(
        o,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], Oe(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), Oe(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), Oe(
        e,
        "title",
        /*label*/
        n[1]
      ), Oe(e, "class", "svelte-1lrphxw"), te(
        e,
        "pending",
        /*pending*/
        n[3]
      ), te(
        e,
        "padded",
        /*padded*/
        n[5]
      ), te(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), te(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), ot(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), ot(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), ot(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(_, c) {
      Zo(_, e, c), s && s.m(e, null), mn(e, t), mn(e, o), Li(l, o, null), i = !0, a || (r = $i(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), a = !0);
    },
    p(_, [c]) {
      /*show_label*/
      _[2] ? s ? s.p(_, c) : (s = Zn(_), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!i || c & /*size*/
      16) && te(
        o,
        "small",
        /*size*/
        _[4] === "small"
      ), (!i || c & /*size*/
      16) && te(
        o,
        "large",
        /*size*/
        _[4] === "large"
      ), (!i || c & /*size*/
      16) && te(
        o,
        "medium",
        /*size*/
        _[4] === "medium"
      ), (!i || c & /*disabled*/
      128) && (e.disabled = /*disabled*/
      _[7]), (!i || c & /*label*/
      2) && Oe(
        e,
        "aria-label",
        /*label*/
        _[1]
      ), (!i || c & /*hasPopup*/
      256) && Oe(
        e,
        "aria-haspopup",
        /*hasPopup*/
        _[8]
      ), (!i || c & /*label*/
      2) && Oe(
        e,
        "title",
        /*label*/
        _[1]
      ), (!i || c & /*pending*/
      8) && te(
        e,
        "pending",
        /*pending*/
        _[3]
      ), (!i || c & /*padded*/
      32) && te(
        e,
        "padded",
        /*padded*/
        _[5]
      ), (!i || c & /*highlight*/
      64) && te(
        e,
        "highlight",
        /*highlight*/
        _[6]
      ), (!i || c & /*transparent*/
      512) && te(
        e,
        "transparent",
        /*transparent*/
        _[9]
      ), c & /*disabled, _color*/
      4224 && ot(e, "color", !/*disabled*/
      _[7] && /*_color*/
      _[12] ? (
        /*_color*/
        _[12]
      ) : "var(--block-label-text-color)"), c & /*disabled, background*/
      1152 && ot(e, "--bg-color", /*disabled*/
      _[7] ? "auto" : (
        /*background*/
        _[10]
      )), c & /*offset*/
      2048 && ot(
        e,
        "margin-left",
        /*offset*/
        _[11] + "px"
      );
    },
    i(_) {
      i || (Di(l.$$.fragment, _), i = !0);
    },
    o(_) {
      Mi(l.$$.fragment, _), i = !1;
    },
    d(_) {
      _ && Xo(e), s && s.d(), Ai(l), a = !1, r();
    }
  };
}
function Pi(n, e, t) {
  let o, { Icon: l } = e, { label: i = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: s = "small" } = e, { padded: _ = !0 } = e, { highlight: c = !1 } = e, { disabled: d = !1 } = e, { hasPopup: u = !1 } = e, { color: g = "var(--block-label-text-color)" } = e, { transparent: T = !1 } = e, { background: k = "var(--background-fill-primary)" } = e, { offset: y = 0 } = e;
  function R(h) {
    Ei.call(this, n, h);
  }
  return n.$$set = (h) => {
    "Icon" in h && t(0, l = h.Icon), "label" in h && t(1, i = h.label), "show_label" in h && t(2, a = h.show_label), "pending" in h && t(3, r = h.pending), "size" in h && t(4, s = h.size), "padded" in h && t(5, _ = h.padded), "highlight" in h && t(6, c = h.highlight), "disabled" in h && t(7, d = h.disabled), "hasPopup" in h && t(8, u = h.hasPopup), "color" in h && t(13, g = h.color), "transparent" in h && t(9, T = h.transparent), "background" in h && t(10, k = h.background), "offset" in h && t(11, y = h.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, o = c ? "var(--color-accent)" : g);
  }, [
    l,
    i,
    a,
    r,
    s,
    _,
    c,
    d,
    u,
    T,
    k,
    y,
    o,
    g,
    R
  ];
}
class Fi extends Ci {
  constructor(e) {
    super(), yi(this, e, Pi, Ii, qi, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: Tr,
  append: Cr,
  attr: Er,
  binding_callbacks: kr,
  create_slot: Ar,
  detach: yr,
  element: $r,
  get_all_dirty_from_scope: Lr,
  get_slot_changes: qr,
  init: Rr,
  insert: Or,
  safe_not_equal: Nr,
  toggle_class: Dr,
  transition_in: Mr,
  transition_out: Ir,
  update_slot_base: Pr
} = window.__gradio__svelte__internal, {
  SvelteComponent: Fr,
  append: Ur,
  attr: zr,
  detach: Hr,
  init: Br,
  insert: Gr,
  noop: Wr,
  safe_not_equal: Vr,
  svg_element: Yr
} = window.__gradio__svelte__internal, {
  SvelteComponent: jr,
  append: Xr,
  attr: Zr,
  detach: Kr,
  init: Jr,
  insert: Qr,
  noop: xr,
  safe_not_equal: e_,
  svg_element: t_
} = window.__gradio__svelte__internal, {
  SvelteComponent: n_,
  append: o_,
  attr: l_,
  detach: i_,
  init: a_,
  insert: s_,
  noop: r_,
  safe_not_equal: __,
  svg_element: f_
} = window.__gradio__svelte__internal, {
  SvelteComponent: c_,
  append: u_,
  attr: d_,
  detach: m_,
  init: p_,
  insert: g_,
  noop: h_,
  safe_not_equal: b_,
  svg_element: w_
} = window.__gradio__svelte__internal, {
  SvelteComponent: v_,
  append: S_,
  attr: T_,
  detach: C_,
  init: E_,
  insert: k_,
  noop: A_,
  safe_not_equal: y_,
  svg_element: $_
} = window.__gradio__svelte__internal, {
  SvelteComponent: L_,
  append: q_,
  attr: R_,
  detach: O_,
  init: N_,
  insert: D_,
  noop: M_,
  safe_not_equal: I_,
  svg_element: P_
} = window.__gradio__svelte__internal, {
  SvelteComponent: F_,
  append: U_,
  attr: z_,
  detach: H_,
  init: B_,
  insert: G_,
  noop: W_,
  safe_not_equal: V_,
  svg_element: Y_
} = window.__gradio__svelte__internal, {
  SvelteComponent: j_,
  append: X_,
  attr: Z_,
  detach: K_,
  init: J_,
  insert: Q_,
  noop: x_,
  safe_not_equal: ef,
  svg_element: tf
} = window.__gradio__svelte__internal, {
  SvelteComponent: nf,
  append: of,
  attr: lf,
  detach: af,
  init: sf,
  insert: rf,
  noop: _f,
  safe_not_equal: ff,
  svg_element: cf
} = window.__gradio__svelte__internal, {
  SvelteComponent: uf,
  append: df,
  attr: mf,
  detach: pf,
  init: gf,
  insert: hf,
  noop: bf,
  safe_not_equal: wf,
  svg_element: vf
} = window.__gradio__svelte__internal, {
  SvelteComponent: Ui,
  append: tn,
  attr: ge,
  detach: zi,
  init: Hi,
  insert: Bi,
  noop: nn,
  safe_not_equal: Gi,
  set_style: ke,
  svg_element: Dt
} = window.__gradio__svelte__internal;
function Wi(n) {
  let e, t, o, l;
  return {
    c() {
      e = Dt("svg"), t = Dt("g"), o = Dt("path"), l = Dt("path"), ge(o, "d", "M18,6L6.087,17.913"), ke(o, "fill", "none"), ke(o, "fill-rule", "nonzero"), ke(o, "stroke-width", "2px"), ge(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), ge(l, "d", "M4.364,4.364L19.636,19.636"), ke(l, "fill", "none"), ke(l, "fill-rule", "nonzero"), ke(l, "stroke-width", "2px"), ge(e, "width", "100%"), ge(e, "height", "100%"), ge(e, "viewBox", "0 0 24 24"), ge(e, "version", "1.1"), ge(e, "xmlns", "http://www.w3.org/2000/svg"), ge(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), ge(e, "xml:space", "preserve"), ge(e, "stroke", "currentColor"), ke(e, "fill-rule", "evenodd"), ke(e, "clip-rule", "evenodd"), ke(e, "stroke-linecap", "round"), ke(e, "stroke-linejoin", "round");
    },
    m(i, a) {
      Bi(i, e, a), tn(e, t), tn(t, o), tn(e, l);
    },
    p: nn,
    i: nn,
    o: nn,
    d(i) {
      i && zi(e);
    }
  };
}
class Vi extends Ui {
  constructor(e) {
    super(), Hi(this, e, null, Wi, Gi, {});
  }
}
const {
  SvelteComponent: Sf,
  append: Tf,
  attr: Cf,
  detach: Ef,
  init: kf,
  insert: Af,
  noop: yf,
  safe_not_equal: $f,
  svg_element: Lf
} = window.__gradio__svelte__internal, {
  SvelteComponent: qf,
  append: Rf,
  attr: Of,
  detach: Nf,
  init: Df,
  insert: Mf,
  noop: If,
  safe_not_equal: Pf,
  svg_element: Ff
} = window.__gradio__svelte__internal, {
  SvelteComponent: Uf,
  append: zf,
  attr: Hf,
  detach: Bf,
  init: Gf,
  insert: Wf,
  noop: Vf,
  safe_not_equal: Yf,
  svg_element: jf
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xf,
  append: Zf,
  attr: Kf,
  detach: Jf,
  init: Qf,
  insert: xf,
  noop: ec,
  safe_not_equal: tc,
  svg_element: nc
} = window.__gradio__svelte__internal, {
  SvelteComponent: oc,
  append: lc,
  attr: ic,
  detach: ac,
  init: sc,
  insert: rc,
  noop: _c,
  safe_not_equal: fc,
  svg_element: cc
} = window.__gradio__svelte__internal, {
  SvelteComponent: uc,
  append: dc,
  attr: mc,
  detach: pc,
  init: gc,
  insert: hc,
  noop: bc,
  safe_not_equal: wc,
  svg_element: vc
} = window.__gradio__svelte__internal, {
  SvelteComponent: Yi,
  append: ji,
  attr: lt,
  detach: Xi,
  init: Zi,
  insert: Ki,
  noop: on,
  safe_not_equal: Ji,
  svg_element: Kn
} = window.__gradio__svelte__internal;
function Qi(n) {
  let e, t;
  return {
    c() {
      e = Kn("svg"), t = Kn("path"), lt(t, "d", "M5 8l4 4 4-4z"), lt(e, "class", "dropdown-arrow svelte-145leq6"), lt(e, "xmlns", "http://www.w3.org/2000/svg"), lt(e, "width", "100%"), lt(e, "height", "100%"), lt(e, "viewBox", "0 0 18 18");
    },
    m(o, l) {
      Ki(o, e, l), ji(e, t);
    },
    p: on,
    i: on,
    o: on,
    d(o) {
      o && Xi(e);
    }
  };
}
class xi extends Yi {
  constructor(e) {
    super(), Zi(this, e, null, Qi, Ji, {});
  }
}
const {
  SvelteComponent: Sc,
  append: Tc,
  attr: Cc,
  detach: Ec,
  init: kc,
  insert: Ac,
  noop: yc,
  safe_not_equal: $c,
  svg_element: Lc
} = window.__gradio__svelte__internal, {
  SvelteComponent: qc,
  append: Rc,
  attr: Oc,
  detach: Nc,
  init: Dc,
  insert: Mc,
  noop: Ic,
  safe_not_equal: Pc,
  svg_element: Fc
} = window.__gradio__svelte__internal, {
  SvelteComponent: Uc,
  append: zc,
  attr: Hc,
  detach: Bc,
  init: Gc,
  insert: Wc,
  noop: Vc,
  safe_not_equal: Yc,
  svg_element: jc
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xc,
  append: Zc,
  attr: Kc,
  detach: Jc,
  init: Qc,
  insert: xc,
  noop: eu,
  safe_not_equal: tu,
  svg_element: nu
} = window.__gradio__svelte__internal, {
  SvelteComponent: ou,
  append: lu,
  attr: iu,
  detach: au,
  init: su,
  insert: ru,
  noop: _u,
  safe_not_equal: fu,
  svg_element: cu
} = window.__gradio__svelte__internal, {
  SvelteComponent: uu,
  append: du,
  attr: mu,
  detach: pu,
  init: gu,
  insert: hu,
  noop: bu,
  safe_not_equal: wu,
  svg_element: vu
} = window.__gradio__svelte__internal, {
  SvelteComponent: Su,
  append: Tu,
  attr: Cu,
  detach: Eu,
  init: ku,
  insert: Au,
  noop: yu,
  safe_not_equal: $u,
  svg_element: Lu
} = window.__gradio__svelte__internal, {
  SvelteComponent: qu,
  append: Ru,
  attr: Ou,
  detach: Nu,
  init: Du,
  insert: Mu,
  noop: Iu,
  safe_not_equal: Pu,
  svg_element: Fu
} = window.__gradio__svelte__internal, {
  SvelteComponent: Uu,
  append: zu,
  attr: Hu,
  detach: Bu,
  init: Gu,
  insert: Wu,
  noop: Vu,
  safe_not_equal: Yu,
  svg_element: ju
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xu,
  append: Zu,
  attr: Ku,
  detach: Ju,
  init: Qu,
  insert: xu,
  noop: ed,
  safe_not_equal: td,
  svg_element: nd
} = window.__gradio__svelte__internal, {
  SvelteComponent: od,
  append: ld,
  attr: id,
  detach: ad,
  init: sd,
  insert: rd,
  noop: _d,
  safe_not_equal: fd,
  svg_element: cd
} = window.__gradio__svelte__internal, {
  SvelteComponent: ud,
  append: dd,
  attr: md,
  detach: pd,
  init: gd,
  insert: hd,
  noop: bd,
  safe_not_equal: wd,
  svg_element: vd
} = window.__gradio__svelte__internal, {
  SvelteComponent: Sd,
  append: Td,
  attr: Cd,
  detach: Ed,
  init: kd,
  insert: Ad,
  noop: yd,
  safe_not_equal: $d,
  svg_element: Ld
} = window.__gradio__svelte__internal, {
  SvelteComponent: qd,
  append: Rd,
  attr: Od,
  detach: Nd,
  init: Dd,
  insert: Md,
  noop: Id,
  safe_not_equal: Pd,
  svg_element: Fd
} = window.__gradio__svelte__internal, {
  SvelteComponent: Ud,
  append: zd,
  attr: Hd,
  detach: Bd,
  init: Gd,
  insert: Wd,
  noop: Vd,
  safe_not_equal: Yd,
  svg_element: jd
} = window.__gradio__svelte__internal, {
  SvelteComponent: Xd,
  append: Zd,
  attr: Kd,
  detach: Jd,
  init: Qd,
  insert: xd,
  noop: em,
  safe_not_equal: tm,
  svg_element: nm
} = window.__gradio__svelte__internal, {
  SvelteComponent: om,
  append: lm,
  attr: im,
  detach: am,
  init: sm,
  insert: rm,
  noop: _m,
  safe_not_equal: fm,
  svg_element: cm
} = window.__gradio__svelte__internal, {
  SvelteComponent: um,
  append: dm,
  attr: mm,
  detach: pm,
  init: gm,
  insert: hm,
  noop: bm,
  safe_not_equal: wm,
  svg_element: vm
} = window.__gradio__svelte__internal, {
  SvelteComponent: Sm,
  append: Tm,
  attr: Cm,
  detach: Em,
  init: km,
  insert: Am,
  noop: ym,
  safe_not_equal: $m,
  svg_element: Lm
} = window.__gradio__svelte__internal, {
  SvelteComponent: qm,
  append: Rm,
  attr: Om,
  detach: Nm,
  init: Dm,
  insert: Mm,
  noop: Im,
  safe_not_equal: Pm,
  svg_element: Fm
} = window.__gradio__svelte__internal, {
  SvelteComponent: Um,
  append: zm,
  attr: Hm,
  detach: Bm,
  init: Gm,
  insert: Wm,
  noop: Vm,
  safe_not_equal: Ym,
  set_style: jm,
  svg_element: Xm
} = window.__gradio__svelte__internal, {
  SvelteComponent: ea,
  append: ta,
  attr: ln,
  detach: na,
  init: oa,
  insert: la,
  noop: an,
  safe_not_equal: ia,
  svg_element: Jn
} = window.__gradio__svelte__internal;
function aa(n) {
  let e, t;
  return {
    c() {
      e = Jn("svg"), t = Jn("path"), ln(t, "d", "M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"), ln(e, "xmlns", "http://www.w3.org/2000/svg"), ln(e, "viewBox", "0 0 24 24");
    },
    m(o, l) {
      la(o, e, l), ta(e, t);
    },
    p: an,
    i: an,
    o: an,
    d(o) {
      o && na(e);
    }
  };
}
class sa extends ea {
  constructor(e) {
    super(), oa(this, e, null, aa, ia, {});
  }
}
const {
  SvelteComponent: Zm,
  append: Km,
  attr: Jm,
  detach: Qm,
  init: xm,
  insert: e0,
  noop: t0,
  safe_not_equal: n0,
  svg_element: o0
} = window.__gradio__svelte__internal, {
  SvelteComponent: l0,
  append: i0,
  attr: a0,
  detach: s0,
  init: r0,
  insert: _0,
  noop: f0,
  safe_not_equal: c0,
  svg_element: u0
} = window.__gradio__svelte__internal, {
  SvelteComponent: d0,
  append: m0,
  attr: p0,
  detach: g0,
  init: h0,
  insert: b0,
  noop: w0,
  safe_not_equal: v0,
  svg_element: S0
} = window.__gradio__svelte__internal, {
  SvelteComponent: T0,
  append: C0,
  attr: E0,
  detach: k0,
  init: A0,
  insert: y0,
  noop: $0,
  safe_not_equal: L0,
  svg_element: q0
} = window.__gradio__svelte__internal, {
  SvelteComponent: R0,
  append: O0,
  attr: N0,
  detach: D0,
  init: M0,
  insert: I0,
  noop: P0,
  safe_not_equal: F0,
  svg_element: U0
} = window.__gradio__svelte__internal, {
  SvelteComponent: z0,
  append: H0,
  attr: B0,
  detach: G0,
  init: W0,
  insert: V0,
  noop: Y0,
  safe_not_equal: j0,
  svg_element: X0
} = window.__gradio__svelte__internal, {
  SvelteComponent: Z0,
  append: K0,
  attr: J0,
  detach: Q0,
  init: x0,
  insert: ep,
  noop: tp,
  safe_not_equal: np,
  svg_element: op
} = window.__gradio__svelte__internal, {
  SvelteComponent: lp,
  append: ip,
  attr: ap,
  detach: sp,
  init: rp,
  insert: _p,
  noop: fp,
  safe_not_equal: cp,
  svg_element: up,
  text: dp
} = window.__gradio__svelte__internal, {
  SvelteComponent: mp,
  append: pp,
  attr: gp,
  detach: hp,
  init: bp,
  insert: wp,
  noop: vp,
  safe_not_equal: Sp,
  svg_element: Tp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Cp,
  append: Ep,
  attr: kp,
  detach: Ap,
  init: yp,
  insert: $p,
  noop: Lp,
  safe_not_equal: qp,
  svg_element: Rp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Op,
  append: Np,
  attr: Dp,
  detach: Mp,
  init: Ip,
  insert: Pp,
  noop: Fp,
  safe_not_equal: Up,
  svg_element: zp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Hp,
  append: Bp,
  attr: Gp,
  detach: Wp,
  init: Vp,
  insert: Yp,
  noop: jp,
  safe_not_equal: Xp,
  svg_element: Zp
} = window.__gradio__svelte__internal, {
  SvelteComponent: Kp,
  append: Jp,
  attr: Qp,
  detach: xp,
  init: e1,
  insert: t1,
  noop: n1,
  safe_not_equal: o1,
  svg_element: l1
} = window.__gradio__svelte__internal, {
  SvelteComponent: i1,
  append: a1,
  attr: s1,
  detach: r1,
  init: _1,
  insert: f1,
  noop: c1,
  safe_not_equal: u1,
  svg_element: d1,
  text: m1
} = window.__gradio__svelte__internal, {
  SvelteComponent: p1,
  append: g1,
  attr: h1,
  detach: b1,
  init: w1,
  insert: v1,
  noop: S1,
  safe_not_equal: T1,
  svg_element: C1,
  text: E1
} = window.__gradio__svelte__internal, {
  SvelteComponent: k1,
  append: A1,
  attr: y1,
  detach: $1,
  init: L1,
  insert: q1,
  noop: R1,
  safe_not_equal: O1,
  svg_element: N1,
  text: D1
} = window.__gradio__svelte__internal, {
  SvelteComponent: M1,
  append: I1,
  attr: P1,
  detach: F1,
  init: U1,
  insert: z1,
  noop: H1,
  safe_not_equal: B1,
  svg_element: G1
} = window.__gradio__svelte__internal, {
  SvelteComponent: W1,
  append: V1,
  attr: Y1,
  detach: j1,
  init: X1,
  insert: Z1,
  noop: K1,
  safe_not_equal: J1,
  svg_element: Q1
} = window.__gradio__svelte__internal, ra = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Qn = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
ra.reduce((n, { color: e, primary: t, secondary: o }) => ({
  ...n,
  [e]: {
    primary: Qn[e][t],
    secondary: Qn[e][o]
  }
}), {});
const {
  SvelteComponent: x1,
  create_component: eg,
  destroy_component: tg,
  init: ng,
  mount_component: og,
  safe_not_equal: lg,
  transition_in: ig,
  transition_out: ag
} = window.__gradio__svelte__internal, { createEventDispatcher: sg } = window.__gradio__svelte__internal, {
  SvelteComponent: rg,
  append: _g,
  attr: fg,
  check_outros: cg,
  create_component: ug,
  destroy_component: dg,
  detach: mg,
  element: pg,
  group_outros: gg,
  init: hg,
  insert: bg,
  mount_component: wg,
  safe_not_equal: vg,
  set_data: Sg,
  space: Tg,
  text: Cg,
  toggle_class: Eg,
  transition_in: kg,
  transition_out: Ag
} = window.__gradio__svelte__internal, {
  SvelteComponent: yg,
  attr: $g,
  create_slot: Lg,
  detach: qg,
  element: Rg,
  get_all_dirty_from_scope: Og,
  get_slot_changes: Ng,
  init: Dg,
  insert: Mg,
  safe_not_equal: Ig,
  toggle_class: Pg,
  transition_in: Fg,
  transition_out: Ug,
  update_slot_base: zg
} = window.__gradio__svelte__internal, {
  SvelteComponent: Hg,
  append: Bg,
  attr: Gg,
  check_outros: Wg,
  create_component: Vg,
  destroy_component: Yg,
  detach: jg,
  element: Xg,
  empty: Zg,
  group_outros: Kg,
  init: Jg,
  insert: Qg,
  listen: xg,
  mount_component: eh,
  safe_not_equal: th,
  space: nh,
  toggle_class: oh,
  transition_in: lh,
  transition_out: ih
} = window.__gradio__svelte__internal;
function Bt() {
}
function _a(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function xn(n) {
  const e = typeof n == "string" && n.match(/^\s*(-?[\d.]+)([^\s]*)\s*$/);
  return e ? [parseFloat(e[1]), e[2] || "px"] : [
    /** @type {number} */
    n,
    "px"
  ];
}
const Ko = typeof window < "u";
let eo = Ko ? () => window.performance.now() : () => Date.now(), Jo = Ko ? (n) => requestAnimationFrame(n) : Bt;
const ft = /* @__PURE__ */ new Set();
function Qo(n) {
  ft.forEach((e) => {
    e.c(n) || (ft.delete(e), e.f());
  }), ft.size !== 0 && Jo(Qo);
}
function fa(n) {
  let e;
  return ft.size === 0 && Jo(Qo), {
    promise: new Promise((t) => {
      ft.add(e = { c: n, f: t });
    }),
    abort() {
      ft.delete(e);
    }
  };
}
function ca(n) {
  const e = n - 1;
  return e * e * e + 1;
}
function to(n, { delay: e = 0, duration: t = 400, easing: o = ca, x: l = 0, y: i = 0, opacity: a = 0 } = {}) {
  const r = getComputedStyle(n), s = +r.opacity, _ = r.transform === "none" ? "" : r.transform, c = s * (1 - a), [d, u] = xn(l), [g, T] = xn(i);
  return {
    delay: e,
    duration: t,
    easing: o,
    css: (k, y) => `
			transform: ${_} translate(${(1 - k) * d}${u}, ${(1 - k) * g}${T});
			opacity: ${s - c * y}`
  };
}
const it = [];
function ua(n, e = Bt) {
  let t;
  const o = /* @__PURE__ */ new Set();
  function l(r) {
    if (_a(n, r) && (n = r, t)) {
      const s = !it.length;
      for (const _ of o)
        _[1](), it.push(_, n);
      if (s) {
        for (let _ = 0; _ < it.length; _ += 2)
          it[_][0](it[_ + 1]);
        it.length = 0;
      }
    }
  }
  function i(r) {
    l(r(n));
  }
  function a(r, s = Bt) {
    const _ = [r, s];
    return o.add(_), o.size === 1 && (t = e(l, i) || Bt), r(n), () => {
      o.delete(_), o.size === 0 && t && (t(), t = null);
    };
  }
  return { set: l, update: i, subscribe: a };
}
function no(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function gn(n, e, t, o) {
  if (typeof t == "number" || no(t)) {
    const l = o - t, i = (t - e) / (n.dt || 1 / 60), a = n.opts.stiffness * l, r = n.opts.damping * i, s = (a - r) * n.inv_mass, _ = (i + s) * n.dt;
    return Math.abs(_) < n.opts.precision && Math.abs(l) < n.opts.precision ? o : (n.settled = !1, no(t) ? new Date(t.getTime() + _) : t + _);
  } else {
    if (Array.isArray(t))
      return t.map(
        (l, i) => gn(n, e[i], t[i], o[i])
      );
    if (typeof t == "object") {
      const l = {};
      for (const i in t)
        l[i] = gn(n, e[i], t[i], o[i]);
      return l;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function oo(n, e = {}) {
  const t = ua(n), { stiffness: o = 0.15, damping: l = 0.8, precision: i = 0.01 } = e;
  let a, r, s, _ = n, c = n, d = 1, u = 0, g = !1;
  function T(y, R = {}) {
    c = y;
    const h = s = {};
    return n == null || R.hard || k.stiffness >= 1 && k.damping >= 1 ? (g = !0, a = eo(), _ = y, t.set(n = c), Promise.resolve()) : (R.soft && (u = 1 / ((R.soft === !0 ? 0.5 : +R.soft) * 60), d = 0), r || (a = eo(), g = !1, r = fa((m) => {
      if (g)
        return g = !1, r = null, !1;
      d = Math.min(d + u, 1);
      const p = {
        inv_mass: d,
        opts: k,
        settled: !0,
        dt: (m - a) * 60 / 1e3
      }, $ = gn(p, _, n, c);
      return a = m, _ = n, t.set(n = $), p.settled && (r = null), !p.settled;
    })), new Promise((m) => {
      r.promise.then(() => {
        h === s && m();
      });
    }));
  }
  const k = {
    set: T,
    update: (y, R) => T(y(c, n), R),
    subscribe: t.subscribe,
    stiffness: o,
    damping: l,
    precision: i
  };
  return k;
}
const {
  SvelteComponent: da,
  add_render_callback: xo,
  append: st,
  attr: W,
  binding_callbacks: lo,
  check_outros: ma,
  create_bidirectional_transition: io,
  destroy_each: pa,
  detach: Et,
  element: At,
  empty: ga,
  ensure_array_like: ao,
  group_outros: ha,
  init: ba,
  insert: kt,
  listen: hn,
  prevent_default: wa,
  run_all: va,
  safe_not_equal: Sa,
  set_data: Ta,
  set_style: se,
  space: Wt,
  text: Ca,
  toggle_class: Ae,
  transition_in: sn,
  transition_out: so
} = window.__gradio__svelte__internal, { createEventDispatcher: Ea } = window.__gradio__svelte__internal;
function ro(n, e, t) {
  const o = n.slice();
  return o[27] = e[t], o;
}
function _o(n) {
  let e, t, o, l, i, a, r, s = ao(
    /*filtered_indices*/
    n[1]
  ), _ = [];
  for (let c = 0; c < s.length; c += 1)
    _[c] = fo(ro(n, s, c));
  return {
    c() {
      e = At("ul"), t = At("li"), t.textContent = "Выбрать все", o = Wt();
      for (let c = 0; c < _.length; c += 1)
        _[c].c();
      W(t, "class", "item select-all svelte-wmd465"), W(t, "data-index", "all"), W(t, "aria-label", "Выбрать все"), W(t, "data-testid", "dropdown-option"), W(t, "role", "option"), W(t, "aria-selected", "false"), se(
        t,
        "width",
        /*input_width*/
        n[8] + "px"
      ), W(e, "class", "options svelte-wmd465"), W(e, "role", "listbox"), se(
        e,
        "top",
        /*top*/
        n[9]
      ), se(
        e,
        "bottom",
        /*bottom*/
        n[10]
      ), se(e, "max-height", `calc(${/*max_height*/
      n[11]}px - var(--window-padding))`), se(
        e,
        "width",
        /*input_width*/
        n[8] + "px"
      );
    },
    m(c, d) {
      kt(c, e, d), st(e, t), st(e, o);
      for (let u = 0; u < _.length; u += 1)
        _[u] && _[u].m(e, null);
      n[23](e), i = !0, a || (r = hn(e, "mousedown", wa(
        /*mousedown_handler*/
        n[22]
      )), a = !0);
    },
    p(c, d) {
      if (d & /*input_width*/
      256 && se(
        t,
        "width",
        /*input_width*/
        c[8] + "px"
      ), d & /*filtered_indices, choices, selected_indices, active_index, input_width*/
      307) {
        s = ao(
          /*filtered_indices*/
          c[1]
        );
        let u;
        for (u = 0; u < s.length; u += 1) {
          const g = ro(c, s, u);
          _[u] ? _[u].p(g, d) : (_[u] = fo(g), _[u].c(), _[u].m(e, null));
        }
        for (; u < _.length; u += 1)
          _[u].d(1);
        _.length = s.length;
      }
      d & /*top*/
      512 && se(
        e,
        "top",
        /*top*/
        c[9]
      ), d & /*bottom*/
      1024 && se(
        e,
        "bottom",
        /*bottom*/
        c[10]
      ), d & /*max_height*/
      2048 && se(e, "max-height", `calc(${/*max_height*/
      c[11]}px - var(--window-padding))`), d & /*input_width*/
      256 && se(
        e,
        "width",
        /*input_width*/
        c[8] + "px"
      );
    },
    i(c) {
      i || (c && xo(() => {
        i && (l || (l = io(e, to, { duration: 200, y: 5 }, !0)), l.run(1));
      }), i = !0);
    },
    o(c) {
      c && (l || (l = io(e, to, { duration: 200, y: 5 }, !1)), l.run(0)), i = !1;
    },
    d(c) {
      c && Et(e), pa(_, c), n[23](null), c && l && l.end(), a = !1, r();
    }
  };
}
function fo(n) {
  let e, t, o, l = (
    /*choices*/
    n[0][
      /*index*/
      n[27]
    ][0] + ""
  ), i, a, r, s, _;
  return {
    c() {
      e = At("li"), t = At("span"), t.textContent = "✓", o = Wt(), i = Ca(l), a = Wt(), W(t, "class", "inner-item svelte-wmd465"), Ae(t, "hide", !/*selected_indices*/
      n[4].includes(
        /*index*/
        n[27]
      )), W(e, "class", "item svelte-wmd465"), W(e, "data-index", r = /*index*/
      n[27]), W(e, "aria-label", s = /*choices*/
      n[0][
        /*index*/
        n[27]
      ][0]), W(e, "data-testid", "dropdown-option"), W(e, "role", "option"), W(e, "aria-selected", _ = /*selected_indices*/
      n[4].includes(
        /*index*/
        n[27]
      )), Ae(
        e,
        "selected",
        /*selected_indices*/
        n[4].includes(
          /*index*/
          n[27]
        )
      ), Ae(
        e,
        "active",
        /*index*/
        n[27] === /*active_index*/
        n[5]
      ), Ae(
        e,
        "bg-gray-100",
        /*index*/
        n[27] === /*active_index*/
        n[5]
      ), Ae(
        e,
        "dark:bg-gray-600",
        /*index*/
        n[27] === /*active_index*/
        n[5]
      ), se(
        e,
        "width",
        /*input_width*/
        n[8] + "px"
      );
    },
    m(c, d) {
      kt(c, e, d), st(e, t), st(e, o), st(e, i), st(e, a);
    },
    p(c, d) {
      d & /*selected_indices, filtered_indices*/
      18 && Ae(t, "hide", !/*selected_indices*/
      c[4].includes(
        /*index*/
        c[27]
      )), d & /*choices, filtered_indices*/
      3 && l !== (l = /*choices*/
      c[0][
        /*index*/
        c[27]
      ][0] + "") && Ta(i, l), d & /*filtered_indices*/
      2 && r !== (r = /*index*/
      c[27]) && W(e, "data-index", r), d & /*choices, filtered_indices*/
      3 && s !== (s = /*choices*/
      c[0][
        /*index*/
        c[27]
      ][0]) && W(e, "aria-label", s), d & /*selected_indices, filtered_indices*/
      18 && _ !== (_ = /*selected_indices*/
      c[4].includes(
        /*index*/
        c[27]
      )) && W(e, "aria-selected", _), d & /*selected_indices, filtered_indices*/
      18 && Ae(
        e,
        "selected",
        /*selected_indices*/
        c[4].includes(
          /*index*/
          c[27]
        )
      ), d & /*filtered_indices, active_index*/
      34 && Ae(
        e,
        "active",
        /*index*/
        c[27] === /*active_index*/
        c[5]
      ), d & /*filtered_indices, active_index*/
      34 && Ae(
        e,
        "bg-gray-100",
        /*index*/
        c[27] === /*active_index*/
        c[5]
      ), d & /*filtered_indices, active_index*/
      34 && Ae(
        e,
        "dark:bg-gray-600",
        /*index*/
        c[27] === /*active_index*/
        c[5]
      ), d & /*input_width*/
      256 && se(
        e,
        "width",
        /*input_width*/
        c[8] + "px"
      );
    },
    d(c) {
      c && Et(e);
    }
  };
}
function ka(n) {
  let e, t, o, l, i;
  xo(
    /*onwindowresize*/
    n[20]
  );
  let a = (
    /*show_options*/
    n[2] && !/*disabled*/
    n[3] && _o(n)
  );
  return {
    c() {
      e = At("div"), t = Wt(), a && a.c(), o = ga(), W(e, "class", "reference");
    },
    m(r, s) {
      kt(r, e, s), n[21](e), kt(r, t, s), a && a.m(r, s), kt(r, o, s), l || (i = [
        hn(
          window,
          "scroll",
          /*scroll_listener*/
          n[13]
        ),
        hn(
          window,
          "resize",
          /*onwindowresize*/
          n[20]
        )
      ], l = !0);
    },
    p(r, [s]) {
      /*show_options*/
      r[2] && !/*disabled*/
      r[3] ? a ? (a.p(r, s), s & /*show_options, disabled*/
      12 && sn(a, 1)) : (a = _o(r), a.c(), sn(a, 1), a.m(o.parentNode, o)) : a && (ha(), so(a, 1, 1, () => {
        a = null;
      }), ma());
    },
    i(r) {
      sn(a);
    },
    o(r) {
      so(a);
    },
    d(r) {
      r && (Et(e), Et(t), Et(o)), n[21](null), a && a.d(r), l = !1, va(i);
    }
  };
}
function Aa(n, e, t) {
  var o, l;
  let { choices: i } = e, { filtered_indices: a } = e, { show_options: r = !1 } = e, { disabled: s = !1 } = e, { selected_indices: _ = [] } = e, { active_index: c = null } = e, d, u, g, T, k, y, R, h, m, p;
  function $() {
    const { top: O, bottom: C } = k.getBoundingClientRect();
    t(17, d = O), t(18, u = p - C);
  }
  let S = null;
  function D() {
    r && (S !== null && clearTimeout(S), S = setTimeout(
      () => {
        $(), S = null;
      },
      10
    ));
  }
  const F = Ea();
  function P() {
    t(12, p = window.innerHeight);
  }
  function Y(O) {
    lo[O ? "unshift" : "push"](() => {
      k = O, t(6, k);
    });
  }
  const M = (O) => F("change", O);
  function X(O) {
    lo[O ? "unshift" : "push"](() => {
      y = O, t(7, y);
    });
  }
  return n.$$set = (O) => {
    "choices" in O && t(0, i = O.choices), "filtered_indices" in O && t(1, a = O.filtered_indices), "show_options" in O && t(2, r = O.show_options), "disabled" in O && t(3, s = O.disabled), "selected_indices" in O && t(4, _ = O.selected_indices), "active_index" in O && t(5, c = O.active_index);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*show_options, refElement, listElement, selected_indices, _a, _b, distance_from_bottom, distance_from_top, input_height*/
    1016020) {
      if (r && k) {
        if (y && _.length > 0) {
          let C = y.querySelectorAll("li");
          for (const ae of Array.from(C))
            if (ae.getAttribute("data-index") === _[0].toString()) {
              t(15, o = y == null ? void 0 : y.scrollTo) === null || o === void 0 || o.call(y, 0, ae.offsetTop);
              break;
            }
        }
        $();
        const O = t(16, l = k.parentElement) === null || l === void 0 ? void 0 : l.getBoundingClientRect();
        t(19, g = (O == null ? void 0 : O.height) || 0), t(8, T = (O == null ? void 0 : O.width) || 0);
      }
      u > d ? (t(9, R = `${d}px`), t(11, m = u), t(10, h = null)) : (t(10, h = `${u + g}px`), t(11, m = d - g), t(9, R = null));
    }
  }, [
    i,
    a,
    r,
    s,
    _,
    c,
    k,
    y,
    T,
    R,
    h,
    m,
    p,
    D,
    F,
    o,
    l,
    d,
    u,
    g,
    P,
    Y,
    M,
    X
  ];
}
class ya extends da {
  constructor(e) {
    super(), ba(this, e, Aa, ka, Sa, {
      choices: 0,
      filtered_indices: 1,
      show_options: 2,
      disabled: 3,
      selected_indices: 4,
      active_index: 5
    });
  }
}
function $a(n, e) {
  return (n % e + e) % e;
}
function La(n, e) {
  return n.reduce((t, o, l) => ((!e || o[0].toLowerCase().includes(e.toLowerCase())) && t.push(l), t), []);
}
function qa(n, e, t) {
  n("change", e), t || n("input");
}
function Ra(n, e, t) {
  if (n.key === "Escape")
    return [!1, e];
  if ((n.key === "ArrowDown" || n.key === "ArrowUp") && t.length >= 0)
    if (e === null)
      e = n.key === "ArrowDown" ? t[0] : t[t.length - 1];
    else {
      const o = t.indexOf(e), l = n.key === "ArrowUp" ? -1 : 1;
      e = t[$a(o + l, t.length)];
    }
  return [!0, e];
}
const {
  SvelteComponent: Oa,
  append: Me,
  attr: _e,
  binding_callbacks: Na,
  check_outros: el,
  create_component: Vt,
  destroy_component: Yt,
  detach: le,
  element: We,
  group_outros: tl,
  init: Da,
  insert: ie,
  listen: Ve,
  mount_component: jt,
  noop: Ma,
  run_all: nl,
  safe_not_equal: Ia,
  set_data: ct,
  set_input_value: co,
  space: rt,
  text: Fe,
  toggle_class: at,
  transition_in: ye,
  transition_out: Ie
} = window.__gradio__svelte__internal, { afterUpdate: Pa, createEventDispatcher: Fa } = window.__gradio__svelte__internal;
function Ua(n) {
  let e;
  return {
    c() {
      e = Fe(
        /*label*/
        n[0]
      );
    },
    m(t, o) {
      ie(t, e, o);
    },
    p(t, o) {
      o[0] & /*label*/
      1 && ct(
        e,
        /*label*/
        t[0]
      );
    },
    d(t) {
      t && le(e);
    }
  };
}
function za(n) {
  let e = (
    /*selected_indices*/
    n[12].length + ""
  ), t, o, l = (
    /*selected_indices*/
    n[12].length % 10 === 1 && /*selected_indices*/
    n[12].length % 100 !== 11 ? "источник" : (
      /*selected_indices*/
      n[12].length % 10 >= 2 && /*selected_indices*/
      n[12].length % 10 <= 4 && /*selected_indices*/
      (n[12].length % 100 < 10 || /*selected_indices*/
      n[12].length % 100 >= 20) ? "источника" : "источников"
    )
  ), i;
  return {
    c() {
      t = Fe(e), o = rt(), i = Fe(l);
    },
    m(a, r) {
      ie(a, t, r), ie(a, o, r), ie(a, i, r);
    },
    p(a, r) {
      r[0] & /*selected_indices*/
      4096 && e !== (e = /*selected_indices*/
      a[12].length + "") && ct(t, e), r[0] & /*selected_indices*/
      4096 && l !== (l = /*selected_indices*/
      a[12].length % 10 === 1 && /*selected_indices*/
      a[12].length % 100 !== 11 ? "источник" : (
        /*selected_indices*/
        a[12].length % 10 >= 2 && /*selected_indices*/
        a[12].length % 10 <= 4 && /*selected_indices*/
        (a[12].length % 100 < 10 || /*selected_indices*/
        a[12].length % 100 >= 20) ? "источника" : "источников"
      )) && ct(i, l);
    },
    d(a) {
      a && (le(t), le(o), le(i));
    }
  };
}
function Ha(n) {
  let e = (
    /*choices_names*/
    n[15][
      /*selected_indices*/
      n[12][0]
    ] + ""
  ), t, o, l = (
    /*choices_names*/
    n[15][
      /*selected_indices*/
      n[12][1]
    ] + ""
  ), i;
  return {
    c() {
      t = Fe(e), o = Fe(", "), i = Fe(l);
    },
    m(a, r) {
      ie(a, t, r), ie(a, o, r), ie(a, i, r);
    },
    p(a, r) {
      r[0] & /*choices_names, selected_indices*/
      36864 && e !== (e = /*choices_names*/
      a[15][
        /*selected_indices*/
        a[12][0]
      ] + "") && ct(t, e), r[0] & /*choices_names, selected_indices*/
      36864 && l !== (l = /*choices_names*/
      a[15][
        /*selected_indices*/
        a[12][1]
      ] + "") && ct(i, l);
    },
    d(a) {
      a && (le(t), le(o), le(i));
    }
  };
}
function Ba(n) {
  let e = (
    /*choices_names*/
    n[15][
      /*selected_indices*/
      n[12][0]
    ] + ""
  ), t;
  return {
    c() {
      t = Fe(e);
    },
    m(o, l) {
      ie(o, t, l);
    },
    p(o, l) {
      l[0] & /*choices_names, selected_indices*/
      36864 && e !== (e = /*choices_names*/
      o[15][
        /*selected_indices*/
        o[12][0]
      ] + "") && ct(t, e);
    },
    d(o) {
      o && le(t);
    }
  };
}
function Ga(n) {
  let e;
  return {
    c() {
      e = Fe("Все источники");
    },
    m(t, o) {
      ie(t, e, o);
    },
    p: Ma,
    d(t) {
      t && le(e);
    }
  };
}
function uo(n) {
  let e, t, o, l, i = (
    /*selected_indices*/
    n[12].length > 0 && mo(n)
  );
  return o = new xi({}), {
    c() {
      i && i.c(), e = rt(), t = We("span"), Vt(o.$$.fragment), _e(t, "class", "icon-wrap svelte-19ik8fr");
    },
    m(a, r) {
      i && i.m(a, r), ie(a, e, r), ie(a, t, r), jt(o, t, null), l = !0;
    },
    p(a, r) {
      /*selected_indices*/
      a[12].length > 0 ? i ? (i.p(a, r), r[0] & /*selected_indices*/
      4096 && ye(i, 1)) : (i = mo(a), i.c(), ye(i, 1), i.m(e.parentNode, e)) : i && (tl(), Ie(i, 1, 1, () => {
        i = null;
      }), el());
    },
    i(a) {
      l || (ye(i), ye(o.$$.fragment, a), l = !0);
    },
    o(a) {
      Ie(i), Ie(o.$$.fragment, a), l = !1;
    },
    d(a) {
      a && (le(e), le(t)), i && i.d(a), Yt(o);
    }
  };
}
function mo(n) {
  let e, t, o, l, i, a;
  return t = new sa({}), {
    c() {
      e = We("div"), Vt(t.$$.fragment), _e(e, "role", "button"), _e(e, "tabindex", "0"), _e(e, "class", "token-remove remove-all svelte-19ik8fr"), _e(e, "title", o = /*i18n*/
      n[9]("common.clear"));
    },
    m(r, s) {
      ie(r, e, s), jt(t, e, null), l = !0, i || (a = [
        Ve(
          e,
          "click",
          /*remove_all*/
          n[20]
        ),
        Ve(
          e,
          "keydown",
          /*keydown_handler*/
          n[34]
        )
      ], i = !0);
    },
    p(r, s) {
      (!l || s[0] & /*i18n*/
      512 && o !== (o = /*i18n*/
      r[9]("common.clear"))) && _e(e, "title", o);
    },
    i(r) {
      l || (ye(t.$$.fragment, r), l = !0);
    },
    o(r) {
      Ie(t.$$.fragment, r), l = !1;
    },
    d(r) {
      r && le(e), Yt(t), i = !1, nl(a);
    }
  };
}
function Wa(n) {
  let e, t, o, l, i, a, r, s, _, c, d, u, g, T, k;
  t = new Ti({
    props: {
      show_label: (
        /*show_label*/
        n[5]
      ),
      info: (
        /*info*/
        n[1]
      ),
      $$slots: { default: [Ua] },
      $$scope: { ctx: n }
    }
  });
  function y(p, $) {
    if (
      /*selected_indices*/
      p[12].length === /*choices_names*/
      p[15].length
    ) return Ga;
    if (
      /*selected_indices*/
      p[12].length === 1
    ) return Ba;
    if (
      /*selected_indices*/
      p[12].length === 2
    ) return Ha;
    if (
      /*selected_indices*/
      p[12].length > 2
    ) return za;
  }
  let R = y(n), h = R && R(n), m = !/*disabled*/
  n[4] && uo(n);
  return u = new ya({
    props: {
      show_options: (
        /*show_options*/
        n[14]
      ),
      choices: (
        /*choices*/
        n[3]
      ),
      filtered_indices: (
        /*filtered_indices*/
        n[11]
      ),
      disabled: (
        /*disabled*/
        n[4]
      ),
      selected_indices: (
        /*selected_indices*/
        n[12]
      ),
      active_index: (
        /*active_index*/
        n[16]
      )
    }
  }), u.$on(
    "change",
    /*handle_option_selected*/
    n[19]
  ), u.$on(
    "select_all",
    /*handle_select_all*/
    n[23]
  ), {
    c() {
      e = We("label"), Vt(t.$$.fragment), o = rt(), l = We("div"), i = We("div"), h && h.c(), a = rt(), r = We("div"), s = We("input"), c = rt(), m && m.c(), d = rt(), Vt(u.$$.fragment), _e(s, "class", "border-none svelte-19ik8fr"), s.disabled = /*disabled*/
      n[4], _e(s, "autocomplete", "off"), s.readOnly = _ = !/*filterable*/
      n[8], at(s, "subdued", !/*choices_names*/
      n[15].includes(
        /*input_text*/
        n[10]
      ) && !/*allow_custom_value*/
      n[7] || /*selected_indices*/
      n[12].length === /*max_choices*/
      n[2]), _e(r, "class", "secondary-wrap svelte-19ik8fr"), _e(i, "class", "wrap-inner svelte-19ik8fr"), at(
        i,
        "show_options",
        /*show_options*/
        n[14]
      ), _e(l, "class", "wrap svelte-19ik8fr"), _e(e, "class", "svelte-19ik8fr"), at(
        e,
        "container",
        /*container*/
        n[6]
      );
    },
    m(p, $) {
      ie(p, e, $), jt(t, e, null), Me(e, o), Me(e, l), Me(l, i), h && h.m(i, null), Me(i, a), Me(i, r), Me(r, s), co(
        s,
        /*input_text*/
        n[10]
      ), n[32](s), Me(r, c), m && m.m(r, null), Me(l, d), jt(u, l, null), g = !0, T || (k = [
        Ve(
          s,
          "input",
          /*input_input_handler*/
          n[31]
        ),
        Ve(
          s,
          "keydown",
          /*handle_key_down*/
          n[22]
        ),
        Ve(
          s,
          "keyup",
          /*keyup_handler*/
          n[33]
        ),
        Ve(
          s,
          "blur",
          /*handle_blur*/
          n[18]
        ),
        Ve(
          s,
          "focus",
          /*handle_focus*/
          n[21]
        )
      ], T = !0);
    },
    p(p, $) {
      const S = {};
      $[0] & /*show_label*/
      32 && (S.show_label = /*show_label*/
      p[5]), $[0] & /*info*/
      2 && (S.info = /*info*/
      p[1]), $[0] & /*label*/
      1 | $[1] & /*$$scope*/
      256 && (S.$$scope = { dirty: $, ctx: p }), t.$set(S), R === (R = y(p)) && h ? h.p(p, $) : (h && h.d(1), h = R && R(p), h && (h.c(), h.m(i, a))), (!g || $[0] & /*disabled*/
      16) && (s.disabled = /*disabled*/
      p[4]), (!g || $[0] & /*filterable*/
      256 && _ !== (_ = !/*filterable*/
      p[8])) && (s.readOnly = _), $[0] & /*input_text*/
      1024 && s.value !== /*input_text*/
      p[10] && co(
        s,
        /*input_text*/
        p[10]
      ), (!g || $[0] & /*choices_names, input_text, allow_custom_value, selected_indices, max_choices*/
      38020) && at(s, "subdued", !/*choices_names*/
      p[15].includes(
        /*input_text*/
        p[10]
      ) && !/*allow_custom_value*/
      p[7] || /*selected_indices*/
      p[12].length === /*max_choices*/
      p[2]), /*disabled*/
      p[4] ? m && (tl(), Ie(m, 1, 1, () => {
        m = null;
      }), el()) : m ? (m.p(p, $), $[0] & /*disabled*/
      16 && ye(m, 1)) : (m = uo(p), m.c(), ye(m, 1), m.m(r, null)), (!g || $[0] & /*show_options*/
      16384) && at(
        i,
        "show_options",
        /*show_options*/
        p[14]
      );
      const D = {};
      $[0] & /*show_options*/
      16384 && (D.show_options = /*show_options*/
      p[14]), $[0] & /*choices*/
      8 && (D.choices = /*choices*/
      p[3]), $[0] & /*filtered_indices*/
      2048 && (D.filtered_indices = /*filtered_indices*/
      p[11]), $[0] & /*disabled*/
      16 && (D.disabled = /*disabled*/
      p[4]), $[0] & /*selected_indices*/
      4096 && (D.selected_indices = /*selected_indices*/
      p[12]), $[0] & /*active_index*/
      65536 && (D.active_index = /*active_index*/
      p[16]), u.$set(D), (!g || $[0] & /*container*/
      64) && at(
        e,
        "container",
        /*container*/
        p[6]
      );
    },
    i(p) {
      g || (ye(t.$$.fragment, p), ye(m), ye(u.$$.fragment, p), g = !0);
    },
    o(p) {
      Ie(t.$$.fragment, p), Ie(m), Ie(u.$$.fragment, p), g = !1;
    },
    d(p) {
      p && le(e), Yt(t), h && h.d(), n[32](null), m && m.d(), Yt(u), T = !1, nl(k);
    }
  };
}
function Va(n, e, t) {
  let { label: o } = e, { info: l = void 0 } = e, { value: i = [] } = e, a = [], { value_is_output: r = !1 } = e, { max_choices: s = null } = e, { choices: _ } = e, c, { disabled: d = !1 } = e, { show_label: u } = e, { container: g = !0 } = e, { allow_custom_value: T = !1 } = e, { filterable: k = !0 } = e, { i18n: y } = e, R, h = "", m = "", p = !1, $, S, D = [], F = null, P = [], Y = [];
  const M = Fa();
  Array.isArray(i) && i.forEach((w) => {
    const B = _.map((de) => de[1]).indexOf(w);
    B !== -1 ? P.push(B) : P.push(w);
  });
  function X() {
    T || t(10, h = ""), T && h !== "" && (C(h), t(10, h = "")), t(14, p = !1), t(16, F = null), M("blur");
  }
  function O(w) {
    t(12, P = P.filter((B) => B !== w)), M("select", {
      index: typeof w == "number" ? w : -1,
      value: typeof w == "number" ? S[w] : w,
      selected: !1
    });
  }
  function C(w) {
    (s === null || P.length < s) && (t(12, P = [...P, w]), M("select", {
      index: typeof w == "number" ? w : -1,
      value: typeof w == "number" ? S[w] : w,
      selected: !0
    })), P.length === s && (t(14, p = !1), t(16, F = null), R.blur());
  }
  function ae(w) {
    const B = w.detail.target.dataset.index;
    B === "all" ? U() : ne(parseInt(B));
  }
  function ne(w) {
    P.includes(w) ? O(w) : C(w), t(10, h = "");
  }
  function Ue(w) {
    t(12, P = []), t(10, h = ""), w.preventDefault();
  }
  function je(w) {
    t(11, D = _.map((B, de) => de)), (s === null || P.length < s) && t(14, p = !0), M("focus");
  }
  function Xe(w) {
    t(14, [p, F] = Ra(w, F, D), p, (t(16, F), t(3, _), t(27, c), t(10, h), t(28, m), t(7, T), t(11, D))), w.key === "Enter" && (F !== null ? ne(F) : T && (C(h), t(10, h = ""))), w.key === "Backspace" && h === "" && t(12, P = [...P.slice(0, -1)]), P.length === s && (t(14, p = !1), t(16, F = null));
  }
  function ze() {
    i === void 0 ? t(12, P = []) : Array.isArray(i) && t(12, P = i.map((w) => {
      const B = S.indexOf(w);
      if (B !== -1)
        return B;
      if (T)
        return w;
    }).filter((w) => w !== void 0));
  }
  function U() {
    t(12, P = _.map((w, B) => B));
  }
  Pa(() => {
    t(25, r = !1);
  });
  function Ze() {
    h = this.value, t(10, h);
  }
  function G(w) {
    Na[w ? "unshift" : "push"](() => {
      R = w, t(13, R);
    });
  }
  const Ke = (w) => M("key_up", { key: w.key, input_value: h }), v = (w) => {
    w.key === "Enter" && Ue(w);
  };
  return n.$$set = (w) => {
    "label" in w && t(0, o = w.label), "info" in w && t(1, l = w.info), "value" in w && t(24, i = w.value), "value_is_output" in w && t(25, r = w.value_is_output), "max_choices" in w && t(2, s = w.max_choices), "choices" in w && t(3, _ = w.choices), "disabled" in w && t(4, d = w.disabled), "show_label" in w && t(5, u = w.show_label), "container" in w && t(6, g = w.container), "allow_custom_value" in w && t(7, T = w.allow_custom_value), "filterable" in w && t(8, k = w.filterable), "i18n" in w && t(9, y = w.i18n);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*choices*/
    8 && (t(15, $ = _.map((w) => w[0])), t(29, S = _.map((w) => w[1]))), n.$$.dirty[0] & /*choices, old_choices, input_text, old_input_text, allow_custom_value, filtered_indices*/
    402656392 && (_ !== c || h !== m) && (t(11, D = La(_, h)), t(27, c = _), t(28, m = h), T || t(16, F = D[0])), n.$$.dirty[0] & /*selected_indices, old_selected_index, choices_values*/
    1610616832 && JSON.stringify(P) != JSON.stringify(Y) && (t(24, i = P.map((w) => typeof w == "number" ? S[w] : w)), t(30, Y = P.slice())), n.$$.dirty[0] & /*value, old_value, value_is_output*/
    117440512 && JSON.stringify(i) != JSON.stringify(a) && (qa(M, i, r), t(26, a = Array.isArray(i) ? i.slice() : i)), n.$$.dirty[0] & /*value*/
    16777216 && ze();
  }, [
    o,
    l,
    s,
    _,
    d,
    u,
    g,
    T,
    k,
    y,
    h,
    D,
    P,
    R,
    p,
    $,
    F,
    M,
    X,
    ae,
    Ue,
    je,
    Xe,
    U,
    i,
    r,
    a,
    c,
    m,
    S,
    Y,
    Ze,
    G,
    Ke,
    v
  ];
}
class Ya extends Oa {
  constructor(e) {
    super(), Da(
      this,
      e,
      Va,
      Wa,
      Ia,
      {
        label: 0,
        info: 1,
        value: 24,
        value_is_output: 25,
        max_choices: 2,
        choices: 3,
        disabled: 4,
        show_label: 5,
        container: 6,
        allow_custom_value: 7,
        filterable: 8,
        i18n: 9
      },
      null,
      [-1, -1]
    );
  }
}
function _t(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let o = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + o;
}
const {
  SvelteComponent: ja,
  append: he,
  attr: I,
  component_subscribe: po,
  detach: Xa,
  element: Za,
  init: Ka,
  insert: Ja,
  noop: go,
  safe_not_equal: Qa,
  set_style: Mt,
  svg_element: be,
  toggle_class: ho
} = window.__gradio__svelte__internal, { onMount: xa } = window.__gradio__svelte__internal;
function es(n) {
  let e, t, o, l, i, a, r, s, _, c, d, u;
  return {
    c() {
      e = Za("div"), t = be("svg"), o = be("g"), l = be("path"), i = be("path"), a = be("path"), r = be("path"), s = be("g"), _ = be("path"), c = be("path"), d = be("path"), u = be("path"), I(l, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), I(l, "fill", "#FF7C00"), I(l, "fill-opacity", "0.4"), I(l, "class", "svelte-43sxxs"), I(i, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), I(i, "fill", "#FF7C00"), I(i, "class", "svelte-43sxxs"), I(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), I(a, "fill", "#FF7C00"), I(a, "fill-opacity", "0.4"), I(a, "class", "svelte-43sxxs"), I(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), I(r, "fill", "#FF7C00"), I(r, "class", "svelte-43sxxs"), Mt(o, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), I(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), I(_, "fill", "#FF7C00"), I(_, "fill-opacity", "0.4"), I(_, "class", "svelte-43sxxs"), I(c, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), I(c, "fill", "#FF7C00"), I(c, "class", "svelte-43sxxs"), I(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), I(d, "fill", "#FF7C00"), I(d, "fill-opacity", "0.4"), I(d, "class", "svelte-43sxxs"), I(u, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), I(u, "fill", "#FF7C00"), I(u, "class", "svelte-43sxxs"), Mt(s, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), I(t, "viewBox", "-1200 -1200 3000 3000"), I(t, "fill", "none"), I(t, "xmlns", "http://www.w3.org/2000/svg"), I(t, "class", "svelte-43sxxs"), I(e, "class", "svelte-43sxxs"), ho(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(g, T) {
      Ja(g, e, T), he(e, t), he(t, o), he(o, l), he(o, i), he(o, a), he(o, r), he(t, s), he(s, _), he(s, c), he(s, d), he(s, u);
    },
    p(g, [T]) {
      T & /*$top*/
      2 && Mt(o, "transform", "translate(" + /*$top*/
      g[1][0] + "px, " + /*$top*/
      g[1][1] + "px)"), T & /*$bottom*/
      4 && Mt(s, "transform", "translate(" + /*$bottom*/
      g[2][0] + "px, " + /*$bottom*/
      g[2][1] + "px)"), T & /*margin*/
      1 && ho(
        e,
        "margin",
        /*margin*/
        g[0]
      );
    },
    i: go,
    o: go,
    d(g) {
      g && Xa(e);
    }
  };
}
function ts(n, e, t) {
  let o, l;
  var i = this && this.__awaiter || function(g, T, k, y) {
    function R(h) {
      return h instanceof k ? h : new k(function(m) {
        m(h);
      });
    }
    return new (k || (k = Promise))(function(h, m) {
      function p(D) {
        try {
          S(y.next(D));
        } catch (F) {
          m(F);
        }
      }
      function $(D) {
        try {
          S(y.throw(D));
        } catch (F) {
          m(F);
        }
      }
      function S(D) {
        D.done ? h(D.value) : R(D.value).then(p, $);
      }
      S((y = y.apply(g, T || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = oo([0, 0]);
  po(n, r, (g) => t(1, o = g));
  const s = oo([0, 0]);
  po(n, s, (g) => t(2, l = g));
  let _;
  function c() {
    return i(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), s.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), s.set([125, -140])]), yield Promise.all([r.set([-125, 0]), s.set([125, -0])]), yield Promise.all([r.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function d() {
    return i(this, void 0, void 0, function* () {
      yield c(), _ || d();
    });
  }
  function u() {
    return i(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), s.set([-125, 0])]), d();
    });
  }
  return xa(() => (u(), () => _ = !0)), n.$$set = (g) => {
    "margin" in g && t(0, a = g.margin);
  }, [a, o, l, r, s];
}
class ns extends ja {
  constructor(e) {
    super(), Ka(this, e, ts, es, Qa, { margin: 0 });
  }
}
const {
  SvelteComponent: os,
  append: Ye,
  attr: Se,
  binding_callbacks: bo,
  check_outros: bn,
  create_component: ol,
  create_slot: ll,
  destroy_component: il,
  destroy_each: al,
  detach: L,
  element: $e,
  empty: ut,
  ensure_array_like: Xt,
  get_all_dirty_from_scope: sl,
  get_slot_changes: rl,
  group_outros: wn,
  init: ls,
  insert: q,
  mount_component: _l,
  noop: vn,
  safe_not_equal: is,
  set_data: ce,
  set_style: Pe,
  space: fe,
  text: H,
  toggle_class: re,
  transition_in: ve,
  transition_out: Le,
  update_slot_base: fl
} = window.__gradio__svelte__internal, { tick: as } = window.__gradio__svelte__internal, { onDestroy: ss } = window.__gradio__svelte__internal, { createEventDispatcher: rs } = window.__gradio__svelte__internal, _s = (n) => ({}), wo = (n) => ({}), fs = (n) => ({}), vo = (n) => ({});
function So(n, e, t) {
  const o = n.slice();
  return o[41] = e[t], o[43] = t, o;
}
function To(n, e, t) {
  const o = n.slice();
  return o[41] = e[t], o;
}
function cs(n) {
  let e, t, o, l, i = (
    /*i18n*/
    n[1]("common.error") + ""
  ), a, r, s;
  t = new Fi({
    props: {
      Icon: Vi,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const _ = (
    /*#slots*/
    n[30].error
  ), c = ll(
    _,
    n,
    /*$$scope*/
    n[29],
    wo
  );
  return {
    c() {
      e = $e("div"), ol(t.$$.fragment), o = fe(), l = $e("span"), a = H(i), r = fe(), c && c.c(), Se(e, "class", "clear-status svelte-v0wucf"), Se(l, "class", "error svelte-v0wucf");
    },
    m(d, u) {
      q(d, e, u), _l(t, e, null), q(d, o, u), q(d, l, u), Ye(l, a), q(d, r, u), c && c.m(d, u), s = !0;
    },
    p(d, u) {
      const g = {};
      u[0] & /*i18n*/
      2 && (g.label = /*i18n*/
      d[1]("common.clear")), t.$set(g), (!s || u[0] & /*i18n*/
      2) && i !== (i = /*i18n*/
      d[1]("common.error") + "") && ce(a, i), c && c.p && (!s || u[0] & /*$$scope*/
      536870912) && fl(
        c,
        _,
        d,
        /*$$scope*/
        d[29],
        s ? rl(
          _,
          /*$$scope*/
          d[29],
          u,
          _s
        ) : sl(
          /*$$scope*/
          d[29]
        ),
        wo
      );
    },
    i(d) {
      s || (ve(t.$$.fragment, d), ve(c, d), s = !0);
    },
    o(d) {
      Le(t.$$.fragment, d), Le(c, d), s = !1;
    },
    d(d) {
      d && (L(e), L(o), L(l), L(r)), il(t), c && c.d(d);
    }
  };
}
function us(n) {
  let e, t, o, l, i, a, r, s, _, c = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Co(n)
  );
  function d(m, p) {
    if (
      /*progress*/
      m[7]
    ) return ps;
    if (
      /*queue_position*/
      m[2] !== null && /*queue_size*/
      m[3] !== void 0 && /*queue_position*/
      m[2] >= 0
    ) return ms;
    if (
      /*queue_position*/
      m[2] === 0
    ) return ds;
  }
  let u = d(n), g = u && u(n), T = (
    /*timer*/
    n[5] && Ao(n)
  );
  const k = [ws, bs], y = [];
  function R(m, p) {
    return (
      /*last_progress_level*/
      m[15] != null ? 0 : (
        /*show_progress*/
        m[6] === "full" ? 1 : -1
      )
    );
  }
  ~(i = R(n)) && (a = y[i] = k[i](n));
  let h = !/*timer*/
  n[5] && No(n);
  return {
    c() {
      c && c.c(), e = fe(), t = $e("div"), g && g.c(), o = fe(), T && T.c(), l = fe(), a && a.c(), r = fe(), h && h.c(), s = ut(), Se(t, "class", "progress-text svelte-v0wucf"), re(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), re(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(m, p) {
      c && c.m(m, p), q(m, e, p), q(m, t, p), g && g.m(t, null), Ye(t, o), T && T.m(t, null), q(m, l, p), ~i && y[i].m(m, p), q(m, r, p), h && h.m(m, p), q(m, s, p), _ = !0;
    },
    p(m, p) {
      /*variant*/
      m[8] === "default" && /*show_eta_bar*/
      m[18] && /*show_progress*/
      m[6] === "full" ? c ? c.p(m, p) : (c = Co(m), c.c(), c.m(e.parentNode, e)) : c && (c.d(1), c = null), u === (u = d(m)) && g ? g.p(m, p) : (g && g.d(1), g = u && u(m), g && (g.c(), g.m(t, o))), /*timer*/
      m[5] ? T ? T.p(m, p) : (T = Ao(m), T.c(), T.m(t, null)) : T && (T.d(1), T = null), (!_ || p[0] & /*variant*/
      256) && re(
        t,
        "meta-text-center",
        /*variant*/
        m[8] === "center"
      ), (!_ || p[0] & /*variant*/
      256) && re(
        t,
        "meta-text",
        /*variant*/
        m[8] === "default"
      );
      let $ = i;
      i = R(m), i === $ ? ~i && y[i].p(m, p) : (a && (wn(), Le(y[$], 1, 1, () => {
        y[$] = null;
      }), bn()), ~i ? (a = y[i], a ? a.p(m, p) : (a = y[i] = k[i](m), a.c()), ve(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      m[5] ? h && (wn(), Le(h, 1, 1, () => {
        h = null;
      }), bn()) : h ? (h.p(m, p), p[0] & /*timer*/
      32 && ve(h, 1)) : (h = No(m), h.c(), ve(h, 1), h.m(s.parentNode, s));
    },
    i(m) {
      _ || (ve(a), ve(h), _ = !0);
    },
    o(m) {
      Le(a), Le(h), _ = !1;
    },
    d(m) {
      m && (L(e), L(t), L(l), L(r), L(s)), c && c.d(m), g && g.d(), T && T.d(), ~i && y[i].d(m), h && h.d(m);
    }
  };
}
function Co(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = $e("div"), Se(e, "class", "eta-bar svelte-v0wucf"), Pe(e, "transform", t);
    },
    m(o, l) {
      q(o, e, l);
    },
    p(o, l) {
      l[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (o[17] || 0) * 100 - 100}%)`) && Pe(e, "transform", t);
    },
    d(o) {
      o && L(e);
    }
  };
}
function ds(n) {
  let e;
  return {
    c() {
      e = H("processing |");
    },
    m(t, o) {
      q(t, e, o);
    },
    p: vn,
    d(t) {
      t && L(e);
    }
  };
}
function ms(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), o, l, i, a;
  return {
    c() {
      e = H("queue: "), o = H(t), l = H("/"), i = H(
        /*queue_size*/
        n[3]
      ), a = H(" |");
    },
    m(r, s) {
      q(r, e, s), q(r, o, s), q(r, l, s), q(r, i, s), q(r, a, s);
    },
    p(r, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && ce(o, t), s[0] & /*queue_size*/
      8 && ce(
        i,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (L(e), L(o), L(l), L(i), L(a));
    }
  };
}
function ps(n) {
  let e, t = Xt(
    /*progress*/
    n[7]
  ), o = [];
  for (let l = 0; l < t.length; l += 1)
    o[l] = ko(To(n, t, l));
  return {
    c() {
      for (let l = 0; l < o.length; l += 1)
        o[l].c();
      e = ut();
    },
    m(l, i) {
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(l, i);
      q(l, e, i);
    },
    p(l, i) {
      if (i[0] & /*progress*/
      128) {
        t = Xt(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = To(l, t, a);
          o[a] ? o[a].p(r, i) : (o[a] = ko(r), o[a].c(), o[a].m(e.parentNode, e));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = t.length;
      }
    },
    d(l) {
      l && L(e), al(o, l);
    }
  };
}
function Eo(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), o, l, i = " ", a;
  function r(c, d) {
    return (
      /*p*/
      c[41].length != null ? hs : gs
    );
  }
  let s = r(n), _ = s(n);
  return {
    c() {
      _.c(), e = fe(), o = H(t), l = H(" | "), a = H(i);
    },
    m(c, d) {
      _.m(c, d), q(c, e, d), q(c, o, d), q(c, l, d), q(c, a, d);
    },
    p(c, d) {
      s === (s = r(c)) && _ ? _.p(c, d) : (_.d(1), _ = s(c), _ && (_.c(), _.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      c[41].unit + "") && ce(o, t);
    },
    d(c) {
      c && (L(e), L(o), L(l), L(a)), _.d(c);
    }
  };
}
function gs(n) {
  let e = _t(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = H(e);
    },
    m(o, l) {
      q(o, t, l);
    },
    p(o, l) {
      l[0] & /*progress*/
      128 && e !== (e = _t(
        /*p*/
        o[41].index || 0
      ) + "") && ce(t, e);
    },
    d(o) {
      o && L(t);
    }
  };
}
function hs(n) {
  let e = _t(
    /*p*/
    n[41].index || 0
  ) + "", t, o, l = _t(
    /*p*/
    n[41].length
  ) + "", i;
  return {
    c() {
      t = H(e), o = H("/"), i = H(l);
    },
    m(a, r) {
      q(a, t, r), q(a, o, r), q(a, i, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = _t(
        /*p*/
        a[41].index || 0
      ) + "") && ce(t, e), r[0] & /*progress*/
      128 && l !== (l = _t(
        /*p*/
        a[41].length
      ) + "") && ce(i, l);
    },
    d(a) {
      a && (L(t), L(o), L(i));
    }
  };
}
function ko(n) {
  let e, t = (
    /*p*/
    n[41].index != null && Eo(n)
  );
  return {
    c() {
      t && t.c(), e = ut();
    },
    m(o, l) {
      t && t.m(o, l), q(o, e, l);
    },
    p(o, l) {
      /*p*/
      o[41].index != null ? t ? t.p(o, l) : (t = Eo(o), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(o) {
      o && L(e), t && t.d(o);
    }
  };
}
function Ao(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), o, l;
  return {
    c() {
      e = H(
        /*formatted_timer*/
        n[20]
      ), o = H(t), l = H("s");
    },
    m(i, a) {
      q(i, e, a), q(i, o, a), q(i, l, a);
    },
    p(i, a) {
      a[0] & /*formatted_timer*/
      1048576 && ce(
        e,
        /*formatted_timer*/
        i[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      i[0] ? `/${/*formatted_eta*/
      i[19]}` : "") && ce(o, t);
    },
    d(i) {
      i && (L(e), L(o), L(l));
    }
  };
}
function bs(n) {
  let e, t;
  return e = new ns({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      ol(e.$$.fragment);
    },
    m(o, l) {
      _l(e, o, l), t = !0;
    },
    p(o, l) {
      const i = {};
      l[0] & /*variant*/
      256 && (i.margin = /*variant*/
      o[8] === "default"), e.$set(i);
    },
    i(o) {
      t || (ve(e.$$.fragment, o), t = !0);
    },
    o(o) {
      Le(e.$$.fragment, o), t = !1;
    },
    d(o) {
      il(e, o);
    }
  };
}
function ws(n) {
  let e, t, o, l, i, a = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && yo(n)
  );
  return {
    c() {
      e = $e("div"), t = $e("div"), r && r.c(), o = fe(), l = $e("div"), i = $e("div"), Se(t, "class", "progress-level-inner svelte-v0wucf"), Se(i, "class", "progress-bar svelte-v0wucf"), Pe(i, "width", a), Se(l, "class", "progress-bar-wrap svelte-v0wucf"), Se(e, "class", "progress-level svelte-v0wucf");
    },
    m(s, _) {
      q(s, e, _), Ye(e, t), r && r.m(t, null), Ye(e, o), Ye(e, l), Ye(l, i), n[31](i);
    },
    p(s, _) {
      /*progress*/
      s[7] != null ? r ? r.p(s, _) : (r = yo(s), r.c(), r.m(t, null)) : r && (r.d(1), r = null), _[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      s[15] * 100}%`) && Pe(i, "width", a);
    },
    i: vn,
    o: vn,
    d(s) {
      s && L(e), r && r.d(), n[31](null);
    }
  };
}
function yo(n) {
  let e, t = Xt(
    /*progress*/
    n[7]
  ), o = [];
  for (let l = 0; l < t.length; l += 1)
    o[l] = Oo(So(n, t, l));
  return {
    c() {
      for (let l = 0; l < o.length; l += 1)
        o[l].c();
      e = ut();
    },
    m(l, i) {
      for (let a = 0; a < o.length; a += 1)
        o[a] && o[a].m(l, i);
      q(l, e, i);
    },
    p(l, i) {
      if (i[0] & /*progress_level, progress*/
      16512) {
        t = Xt(
          /*progress*/
          l[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = So(l, t, a);
          o[a] ? o[a].p(r, i) : (o[a] = Oo(r), o[a].c(), o[a].m(e.parentNode, e));
        }
        for (; a < o.length; a += 1)
          o[a].d(1);
        o.length = t.length;
      }
    },
    d(l) {
      l && L(e), al(o, l);
    }
  };
}
function $o(n) {
  let e, t, o, l, i = (
    /*i*/
    n[43] !== 0 && vs()
  ), a = (
    /*p*/
    n[41].desc != null && Lo(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && qo()
  ), s = (
    /*progress_level*/
    n[14] != null && Ro(n)
  );
  return {
    c() {
      i && i.c(), e = fe(), a && a.c(), t = fe(), r && r.c(), o = fe(), s && s.c(), l = ut();
    },
    m(_, c) {
      i && i.m(_, c), q(_, e, c), a && a.m(_, c), q(_, t, c), r && r.m(_, c), q(_, o, c), s && s.m(_, c), q(_, l, c);
    },
    p(_, c) {
      /*p*/
      _[41].desc != null ? a ? a.p(_, c) : (a = Lo(_), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      _[41].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[43]
      ] != null ? r || (r = qo(), r.c(), r.m(o.parentNode, o)) : r && (r.d(1), r = null), /*progress_level*/
      _[14] != null ? s ? s.p(_, c) : (s = Ro(_), s.c(), s.m(l.parentNode, l)) : s && (s.d(1), s = null);
    },
    d(_) {
      _ && (L(e), L(t), L(o), L(l)), i && i.d(_), a && a.d(_), r && r.d(_), s && s.d(_);
    }
  };
}
function vs(n) {
  let e;
  return {
    c() {
      e = H(" /");
    },
    m(t, o) {
      q(t, e, o);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Lo(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = H(e);
    },
    m(o, l) {
      q(o, t, l);
    },
    p(o, l) {
      l[0] & /*progress*/
      128 && e !== (e = /*p*/
      o[41].desc + "") && ce(t, e);
    },
    d(o) {
      o && L(t);
    }
  };
}
function qo(n) {
  let e;
  return {
    c() {
      e = H("-");
    },
    m(t, o) {
      q(t, e, o);
    },
    d(t) {
      t && L(e);
    }
  };
}
function Ro(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, o;
  return {
    c() {
      t = H(e), o = H("%");
    },
    m(l, i) {
      q(l, t, i), q(l, o, i);
    },
    p(l, i) {
      i[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (l[14][
        /*i*/
        l[43]
      ] || 0)).toFixed(1) + "") && ce(t, e);
    },
    d(l) {
      l && (L(t), L(o));
    }
  };
}
function Oo(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && $o(n)
  );
  return {
    c() {
      t && t.c(), e = ut();
    },
    m(o, l) {
      t && t.m(o, l), q(o, e, l);
    },
    p(o, l) {
      /*p*/
      o[41].desc != null || /*progress_level*/
      o[14] && /*progress_level*/
      o[14][
        /*i*/
        o[43]
      ] != null ? t ? t.p(o, l) : (t = $o(o), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(o) {
      o && L(e), t && t.d(o);
    }
  };
}
function No(n) {
  let e, t, o, l;
  const i = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), a = ll(
    i,
    n,
    /*$$scope*/
    n[29],
    vo
  );
  return {
    c() {
      e = $e("p"), t = H(
        /*loading_text*/
        n[9]
      ), o = fe(), a && a.c(), Se(e, "class", "loading svelte-v0wucf");
    },
    m(r, s) {
      q(r, e, s), Ye(e, t), q(r, o, s), a && a.m(r, s), l = !0;
    },
    p(r, s) {
      (!l || s[0] & /*loading_text*/
      512) && ce(
        t,
        /*loading_text*/
        r[9]
      ), a && a.p && (!l || s[0] & /*$$scope*/
      536870912) && fl(
        a,
        i,
        r,
        /*$$scope*/
        r[29],
        l ? rl(
          i,
          /*$$scope*/
          r[29],
          s,
          fs
        ) : sl(
          /*$$scope*/
          r[29]
        ),
        vo
      );
    },
    i(r) {
      l || (ve(a, r), l = !0);
    },
    o(r) {
      Le(a, r), l = !1;
    },
    d(r) {
      r && (L(e), L(o)), a && a.d(r);
    }
  };
}
function Ss(n) {
  let e, t, o, l, i;
  const a = [us, cs], r = [];
  function s(_, c) {
    return (
      /*status*/
      _[4] === "pending" ? 0 : (
        /*status*/
        _[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(n)) && (o = r[t] = a[t](n)), {
    c() {
      e = $e("div"), o && o.c(), Se(e, "class", l = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-v0wucf"), re(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), re(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), re(
        e,
        "generating",
        /*status*/
        n[4] === "generating" && /*show_progress*/
        n[6] === "full"
      ), re(
        e,
        "border",
        /*border*/
        n[12]
      ), Pe(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), Pe(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(_, c) {
      q(_, e, c), ~t && r[t].m(e, null), n[33](e), i = !0;
    },
    p(_, c) {
      let d = t;
      t = s(_), t === d ? ~t && r[t].p(_, c) : (o && (wn(), Le(r[d], 1, 1, () => {
        r[d] = null;
      }), bn()), ~t ? (o = r[t], o ? o.p(_, c) : (o = r[t] = a[t](_), o.c()), ve(o, 1), o.m(e, null)) : o = null), (!i || c[0] & /*variant, show_progress*/
      320 && l !== (l = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-v0wucf")) && Se(e, "class", l), (!i || c[0] & /*variant, show_progress, status, show_progress*/
      336) && re(e, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!i || c[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && re(
        e,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!i || c[0] & /*variant, show_progress, status, show_progress*/
      336) && re(
        e,
        "generating",
        /*status*/
        _[4] === "generating" && /*show_progress*/
        _[6] === "full"
      ), (!i || c[0] & /*variant, show_progress, border*/
      4416) && re(
        e,
        "border",
        /*border*/
        _[12]
      ), c[0] & /*absolute*/
      1024 && Pe(
        e,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), c[0] & /*absolute*/
      1024 && Pe(
        e,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      i || (ve(o), i = !0);
    },
    o(_) {
      Le(o), i = !1;
    },
    d(_) {
      _ && L(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var Ts = function(n, e, t, o) {
  function l(i) {
    return i instanceof t ? i : new t(function(a) {
      a(i);
    });
  }
  return new (t || (t = Promise))(function(i, a) {
    function r(c) {
      try {
        _(o.next(c));
      } catch (d) {
        a(d);
      }
    }
    function s(c) {
      try {
        _(o.throw(c));
      } catch (d) {
        a(d);
      }
    }
    function _(c) {
      c.done ? i(c.value) : l(c.value).then(r, s);
    }
    _((o = o.apply(n, e || [])).next());
  });
};
let It = [], rn = !1;
function Cs(n) {
  return Ts(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (It.push(e), !rn) rn = !0;
      else return;
      yield as(), requestAnimationFrame(() => {
        let o = [0, 0];
        for (let l = 0; l < It.length; l++) {
          const a = It[l].getBoundingClientRect();
          (l === 0 || a.top + window.scrollY <= o[0]) && (o[0] = a.top + window.scrollY, o[1] = l);
        }
        window.scrollTo({ top: o[0] - 20, behavior: "smooth" }), rn = !1, It = [];
      });
    }
  });
}
function Es(n, e, t) {
  let o, { $$slots: l = {}, $$scope: i } = e;
  this && this.__awaiter;
  const a = rs();
  let { i18n: r } = e, { eta: s = null } = e, { queue_position: _ } = e, { queue_size: c } = e, { status: d } = e, { scroll_to_output: u = !1 } = e, { timer: g = !0 } = e, { show_progress: T = "full" } = e, { message: k = null } = e, { progress: y = null } = e, { variant: R = "default" } = e, { loading_text: h = "Loading..." } = e, { absolute: m = !0 } = e, { translucent: p = !1 } = e, { border: $ = !1 } = e, { autoscroll: S } = e, D, F = !1, P = 0, Y = 0, M = null, X = null, O = 0, C = null, ae, ne = null, Ue = !0;
  const je = () => {
    t(0, s = t(27, M = t(19, U = null))), t(25, P = performance.now()), t(26, Y = 0), F = !0, Xe();
  };
  function Xe() {
    requestAnimationFrame(() => {
      t(26, Y = (performance.now() - P) / 1e3), F && Xe();
    });
  }
  function ze() {
    t(26, Y = 0), t(0, s = t(27, M = t(19, U = null))), F && (F = !1);
  }
  ss(() => {
    F && ze();
  });
  let U = null;
  function Ze(v) {
    bo[v ? "unshift" : "push"](() => {
      ne = v, t(16, ne), t(7, y), t(14, C), t(15, ae);
    });
  }
  const G = () => {
    a("clear_status");
  };
  function Ke(v) {
    bo[v ? "unshift" : "push"](() => {
      D = v, t(13, D);
    });
  }
  return n.$$set = (v) => {
    "i18n" in v && t(1, r = v.i18n), "eta" in v && t(0, s = v.eta), "queue_position" in v && t(2, _ = v.queue_position), "queue_size" in v && t(3, c = v.queue_size), "status" in v && t(4, d = v.status), "scroll_to_output" in v && t(22, u = v.scroll_to_output), "timer" in v && t(5, g = v.timer), "show_progress" in v && t(6, T = v.show_progress), "message" in v && t(23, k = v.message), "progress" in v && t(7, y = v.progress), "variant" in v && t(8, R = v.variant), "loading_text" in v && t(9, h = v.loading_text), "absolute" in v && t(10, m = v.absolute), "translucent" in v && t(11, p = v.translucent), "border" in v && t(12, $ = v.border), "autoscroll" in v && t(24, S = v.autoscroll), "$$scope" in v && t(29, i = v.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = M), s != null && M !== s && (t(28, X = (performance.now() - P) / 1e3 + s), t(19, U = X.toFixed(1)), t(27, M = s))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, O = X === null || X <= 0 || !Y ? null : Math.min(Y / X, 1)), n.$$.dirty[0] & /*progress*/
    128 && y != null && t(18, Ue = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? t(14, C = y.map((v) => {
      if (v.index != null && v.length != null)
        return v.index / v.length;
      if (v.progress != null)
        return v.progress;
    })) : t(14, C = null), C ? (t(15, ae = C[C.length - 1]), ne && (ae === 0 ? t(16, ne.style.transition = "0", ne) : t(16, ne.style.transition = "150ms", ne))) : t(15, ae = void 0)), n.$$.dirty[0] & /*status*/
    16 && (d === "pending" ? je() : ze()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && D && u && (d === "pending" || d === "complete") && Cs(D, S), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, o = Y.toFixed(1));
  }, [
    s,
    r,
    _,
    c,
    d,
    g,
    T,
    y,
    R,
    h,
    m,
    p,
    $,
    D,
    C,
    ae,
    ne,
    O,
    Ue,
    U,
    o,
    a,
    u,
    k,
    S,
    P,
    Y,
    M,
    X,
    i,
    l,
    Ze,
    G,
    Ke
  ];
}
class ks extends os {
  constructor(e) {
    super(), ls(
      this,
      e,
      Es,
      Ss,
      is,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
/*! @license DOMPurify 3.2.4 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.2.4/LICENSE */
const {
  entries: cl,
  setPrototypeOf: Do,
  isFrozen: As,
  getPrototypeOf: ys,
  getOwnPropertyDescriptor: $s
} = Object;
let {
  freeze: Q,
  seal: ue,
  create: ul
} = Object, {
  apply: Sn,
  construct: Tn
} = typeof Reflect < "u" && Reflect;
Q || (Q = function(e) {
  return e;
});
ue || (ue = function(e) {
  return e;
});
Sn || (Sn = function(e, t, o) {
  return e.apply(t, o);
});
Tn || (Tn = function(e, t) {
  return new e(...t);
});
const Pt = x(Array.prototype.forEach), Ls = x(Array.prototype.lastIndexOf), Mo = x(Array.prototype.pop), bt = x(Array.prototype.push), qs = x(Array.prototype.splice), Gt = x(String.prototype.toLowerCase), _n = x(String.prototype.toString), Io = x(String.prototype.match), wt = x(String.prototype.replace), Rs = x(String.prototype.indexOf), Os = x(String.prototype.trim), we = x(Object.prototype.hasOwnProperty), J = x(RegExp.prototype.test), vt = Ns(TypeError);
function x(n) {
  return function(e) {
    for (var t = arguments.length, o = new Array(t > 1 ? t - 1 : 0), l = 1; l < t; l++)
      o[l - 1] = arguments[l];
    return Sn(n, e, o);
  };
}
function Ns(n) {
  return function() {
    for (var e = arguments.length, t = new Array(e), o = 0; o < e; o++)
      t[o] = arguments[o];
    return Tn(n, t);
  };
}
function N(n, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : Gt;
  Do && Do(n, null);
  let o = e.length;
  for (; o--; ) {
    let l = e[o];
    if (typeof l == "string") {
      const i = t(l);
      i !== l && (As(e) || (e[o] = i), l = i);
    }
    n[l] = !0;
  }
  return n;
}
function Ds(n) {
  for (let e = 0; e < n.length; e++)
    we(n, e) || (n[e] = null);
  return n;
}
function Ge(n) {
  const e = ul(null);
  for (const [t, o] of cl(n))
    we(n, t) && (Array.isArray(o) ? e[t] = Ds(o) : o && typeof o == "object" && o.constructor === Object ? e[t] = Ge(o) : e[t] = o);
  return e;
}
function St(n, e) {
  for (; n !== null; ) {
    const o = $s(n, e);
    if (o) {
      if (o.get)
        return x(o.get);
      if (typeof o.value == "function")
        return x(o.value);
    }
    n = ys(n);
  }
  function t() {
    return null;
  }
  return t;
}
const Po = Q(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), fn = Q(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), cn = Q(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), Ms = Q(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), un = Q(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), Is = Q(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), Fo = Q(["#text"]), Uo = Q(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), dn = Q(["accent-height", "accumulate", "additive", "alignment-baseline", "amplitude", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "exponent", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "intercept", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "slope", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "tablevalues", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), zo = Q(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), Ft = Q(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), Ps = ue(/\{\{[\w\W]*|[\w\W]*\}\}/gm), Fs = ue(/<%[\w\W]*|[\w\W]*%>/gm), Us = ue(/\$\{[\w\W]*/gm), zs = ue(/^data-[\-\w.\u00B7-\uFFFF]+$/), Hs = ue(/^aria-[\-\w]+$/), dl = ue(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), Bs = ue(/^(?:\w+script|data):/i), Gs = ue(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), ml = ue(/^html$/i), Ws = ue(/^[a-z][.\w]*(-[.\w]+)+$/i);
var Ho = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  ARIA_ATTR: Hs,
  ATTR_WHITESPACE: Gs,
  CUSTOM_ELEMENT: Ws,
  DATA_ATTR: zs,
  DOCTYPE_NAME: ml,
  ERB_EXPR: Fs,
  IS_ALLOWED_URI: dl,
  IS_SCRIPT_OR_DATA: Bs,
  MUSTACHE_EXPR: Ps,
  TMPLIT_EXPR: Us
});
const Tt = {
  element: 1,
  text: 3,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9
}, Vs = function() {
  return typeof window > "u" ? null : window;
}, Ys = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let o = null;
  const l = "data-tt-policy-suffix";
  t && t.hasAttribute(l) && (o = t.getAttribute(l));
  const i = "dompurify" + (o ? "#" + o : "");
  try {
    return e.createPolicy(i, {
      createHTML(a) {
        return a;
      },
      createScriptURL(a) {
        return a;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + i + " could not be created."), null;
  }
}, Bo = function() {
  return {
    afterSanitizeAttributes: [],
    afterSanitizeElements: [],
    afterSanitizeShadowDOM: [],
    beforeSanitizeAttributes: [],
    beforeSanitizeElements: [],
    beforeSanitizeShadowDOM: [],
    uponSanitizeAttribute: [],
    uponSanitizeElement: [],
    uponSanitizeShadowNode: []
  };
};
function pl() {
  let n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : Vs();
  const e = (A) => pl(A);
  if (e.version = "3.2.4", e.removed = [], !n || !n.document || n.document.nodeType !== Tt.document || !n.Element)
    return e.isSupported = !1, e;
  let {
    document: t
  } = n;
  const o = t, l = o.currentScript, {
    DocumentFragment: i,
    HTMLTemplateElement: a,
    Node: r,
    Element: s,
    NodeFilter: _,
    NamedNodeMap: c = n.NamedNodeMap || n.MozNamedAttrMap,
    HTMLFormElement: d,
    DOMParser: u,
    trustedTypes: g
  } = n, T = s.prototype, k = St(T, "cloneNode"), y = St(T, "remove"), R = St(T, "nextSibling"), h = St(T, "childNodes"), m = St(T, "parentNode");
  if (typeof a == "function") {
    const A = t.createElement("template");
    A.content && A.content.ownerDocument && (t = A.content.ownerDocument);
  }
  let p, $ = "";
  const {
    implementation: S,
    createNodeIterator: D,
    createDocumentFragment: F,
    getElementsByTagName: P
  } = t, {
    importNode: Y
  } = o;
  let M = Bo();
  e.isSupported = typeof cl == "function" && typeof m == "function" && S && S.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: X,
    ERB_EXPR: O,
    TMPLIT_EXPR: C,
    DATA_ATTR: ae,
    ARIA_ATTR: ne,
    IS_SCRIPT_OR_DATA: Ue,
    ATTR_WHITESPACE: je,
    CUSTOM_ELEMENT: Xe
  } = Ho;
  let {
    IS_ALLOWED_URI: ze
  } = Ho, U = null;
  const Ze = N({}, [...Po, ...fn, ...cn, ...un, ...Fo]);
  let G = null;
  const Ke = N({}, [...Uo, ...dn, ...zo, ...Ft]);
  let v = Object.seal(ul(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), w = null, B = null, de = !0, dt = !0, Ne = !1, He = !0, De = !1, mt = !0, me = !1, pe = !1, Be = !1, Je = !1, yt = !1, $t = !1, $n = !0, Ln = !1;
  const gl = "user-content-";
  let Zt = !0, pt = !1, Qe = {}, xe = null;
  const qn = N({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let Rn = null;
  const On = N({}, ["audio", "video", "img", "source", "image", "track"]);
  let Kt = null;
  const Nn = N({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), Lt = "http://www.w3.org/1998/Math/MathML", qt = "http://www.w3.org/2000/svg", qe = "http://www.w3.org/1999/xhtml";
  let et = qe, Jt = !1, Qt = null;
  const hl = N({}, [Lt, qt, qe], _n);
  let Rt = N({}, ["mi", "mo", "mn", "ms", "mtext"]), Ot = N({}, ["annotation-xml"]);
  const bl = N({}, ["title", "style", "font", "a", "script"]);
  let gt = null;
  const wl = ["application/xhtml+xml", "text/html"], vl = "text/html";
  let V = null, tt = null;
  const Sl = t.createElement("form"), Dn = function(f) {
    return f instanceof RegExp || f instanceof Function;
  }, xt = function() {
    let f = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(tt && tt === f)) {
      if ((!f || typeof f != "object") && (f = {}), f = Ge(f), gt = // eslint-disable-next-line unicorn/prefer-includes
      wl.indexOf(f.PARSER_MEDIA_TYPE) === -1 ? vl : f.PARSER_MEDIA_TYPE, V = gt === "application/xhtml+xml" ? _n : Gt, U = we(f, "ALLOWED_TAGS") ? N({}, f.ALLOWED_TAGS, V) : Ze, G = we(f, "ALLOWED_ATTR") ? N({}, f.ALLOWED_ATTR, V) : Ke, Qt = we(f, "ALLOWED_NAMESPACES") ? N({}, f.ALLOWED_NAMESPACES, _n) : hl, Kt = we(f, "ADD_URI_SAFE_ATTR") ? N(Ge(Nn), f.ADD_URI_SAFE_ATTR, V) : Nn, Rn = we(f, "ADD_DATA_URI_TAGS") ? N(Ge(On), f.ADD_DATA_URI_TAGS, V) : On, xe = we(f, "FORBID_CONTENTS") ? N({}, f.FORBID_CONTENTS, V) : qn, w = we(f, "FORBID_TAGS") ? N({}, f.FORBID_TAGS, V) : {}, B = we(f, "FORBID_ATTR") ? N({}, f.FORBID_ATTR, V) : {}, Qe = we(f, "USE_PROFILES") ? f.USE_PROFILES : !1, de = f.ALLOW_ARIA_ATTR !== !1, dt = f.ALLOW_DATA_ATTR !== !1, Ne = f.ALLOW_UNKNOWN_PROTOCOLS || !1, He = f.ALLOW_SELF_CLOSE_IN_ATTR !== !1, De = f.SAFE_FOR_TEMPLATES || !1, mt = f.SAFE_FOR_XML !== !1, me = f.WHOLE_DOCUMENT || !1, Je = f.RETURN_DOM || !1, yt = f.RETURN_DOM_FRAGMENT || !1, $t = f.RETURN_TRUSTED_TYPE || !1, Be = f.FORCE_BODY || !1, $n = f.SANITIZE_DOM !== !1, Ln = f.SANITIZE_NAMED_PROPS || !1, Zt = f.KEEP_CONTENT !== !1, pt = f.IN_PLACE || !1, ze = f.ALLOWED_URI_REGEXP || dl, et = f.NAMESPACE || qe, Rt = f.MATHML_TEXT_INTEGRATION_POINTS || Rt, Ot = f.HTML_INTEGRATION_POINTS || Ot, v = f.CUSTOM_ELEMENT_HANDLING || {}, f.CUSTOM_ELEMENT_HANDLING && Dn(f.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (v.tagNameCheck = f.CUSTOM_ELEMENT_HANDLING.tagNameCheck), f.CUSTOM_ELEMENT_HANDLING && Dn(f.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (v.attributeNameCheck = f.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), f.CUSTOM_ELEMENT_HANDLING && typeof f.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (v.allowCustomizedBuiltInElements = f.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), De && (dt = !1), yt && (Je = !0), Qe && (U = N({}, Fo), G = [], Qe.html === !0 && (N(U, Po), N(G, Uo)), Qe.svg === !0 && (N(U, fn), N(G, dn), N(G, Ft)), Qe.svgFilters === !0 && (N(U, cn), N(G, dn), N(G, Ft)), Qe.mathMl === !0 && (N(U, un), N(G, zo), N(G, Ft))), f.ADD_TAGS && (U === Ze && (U = Ge(U)), N(U, f.ADD_TAGS, V)), f.ADD_ATTR && (G === Ke && (G = Ge(G)), N(G, f.ADD_ATTR, V)), f.ADD_URI_SAFE_ATTR && N(Kt, f.ADD_URI_SAFE_ATTR, V), f.FORBID_CONTENTS && (xe === qn && (xe = Ge(xe)), N(xe, f.FORBID_CONTENTS, V)), Zt && (U["#text"] = !0), me && N(U, ["html", "head", "body"]), U.table && (N(U, ["tbody"]), delete w.tbody), f.TRUSTED_TYPES_POLICY) {
        if (typeof f.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw vt('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof f.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw vt('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        p = f.TRUSTED_TYPES_POLICY, $ = p.createHTML("");
      } else
        p === void 0 && (p = Ys(g, l)), p !== null && typeof $ == "string" && ($ = p.createHTML(""));
      Q && Q(f), tt = f;
    }
  }, Mn = N({}, [...fn, ...cn, ...Ms]), In = N({}, [...un, ...Is]), Tl = function(f) {
    let b = m(f);
    (!b || !b.tagName) && (b = {
      namespaceURI: et,
      tagName: "template"
    });
    const E = Gt(f.tagName), z = Gt(b.tagName);
    return Qt[f.namespaceURI] ? f.namespaceURI === qt ? b.namespaceURI === qe ? E === "svg" : b.namespaceURI === Lt ? E === "svg" && (z === "annotation-xml" || Rt[z]) : !!Mn[E] : f.namespaceURI === Lt ? b.namespaceURI === qe ? E === "math" : b.namespaceURI === qt ? E === "math" && Ot[z] : !!In[E] : f.namespaceURI === qe ? b.namespaceURI === qt && !Ot[z] || b.namespaceURI === Lt && !Rt[z] ? !1 : !In[E] && (bl[E] || !Mn[E]) : !!(gt === "application/xhtml+xml" && Qt[f.namespaceURI]) : !1;
  }, Te = function(f) {
    bt(e.removed, {
      element: f
    });
    try {
      m(f).removeChild(f);
    } catch {
      y(f);
    }
  }, Nt = function(f, b) {
    try {
      bt(e.removed, {
        attribute: b.getAttributeNode(f),
        from: b
      });
    } catch {
      bt(e.removed, {
        attribute: null,
        from: b
      });
    }
    if (b.removeAttribute(f), f === "is")
      if (Je || yt)
        try {
          Te(b);
        } catch {
        }
      else
        try {
          b.setAttribute(f, "");
        } catch {
        }
  }, Pn = function(f) {
    let b = null, E = null;
    if (Be)
      f = "<remove></remove>" + f;
    else {
      const j = Io(f, /^[\r\n\t ]+/);
      E = j && j[0];
    }
    gt === "application/xhtml+xml" && et === qe && (f = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + f + "</body></html>");
    const z = p ? p.createHTML(f) : f;
    if (et === qe)
      try {
        b = new u().parseFromString(z, gt);
      } catch {
      }
    if (!b || !b.documentElement) {
      b = S.createDocument(et, "template", null);
      try {
        b.documentElement.innerHTML = Jt ? $ : z;
      } catch {
      }
    }
    const Z = b.body || b.documentElement;
    return f && E && Z.insertBefore(t.createTextNode(E), Z.childNodes[0] || null), et === qe ? P.call(b, me ? "html" : "body")[0] : me ? b.documentElement : Z;
  }, Fn = function(f) {
    return D.call(
      f.ownerDocument || f,
      f,
      // eslint-disable-next-line no-bitwise
      _.SHOW_ELEMENT | _.SHOW_COMMENT | _.SHOW_TEXT | _.SHOW_PROCESSING_INSTRUCTION | _.SHOW_CDATA_SECTION,
      null
    );
  }, en = function(f) {
    return f instanceof d && (typeof f.nodeName != "string" || typeof f.textContent != "string" || typeof f.removeChild != "function" || !(f.attributes instanceof c) || typeof f.removeAttribute != "function" || typeof f.setAttribute != "function" || typeof f.namespaceURI != "string" || typeof f.insertBefore != "function" || typeof f.hasChildNodes != "function");
  }, Un = function(f) {
    return typeof r == "function" && f instanceof r;
  };
  function Re(A, f, b) {
    Pt(A, (E) => {
      E.call(e, f, b, tt);
    });
  }
  const zn = function(f) {
    let b = null;
    if (Re(M.beforeSanitizeElements, f, null), en(f))
      return Te(f), !0;
    const E = V(f.nodeName);
    if (Re(M.uponSanitizeElement, f, {
      tagName: E,
      allowedTags: U
    }), f.hasChildNodes() && !Un(f.firstElementChild) && J(/<[/\w]/g, f.innerHTML) && J(/<[/\w]/g, f.textContent) || f.nodeType === Tt.progressingInstruction || mt && f.nodeType === Tt.comment && J(/<[/\w]/g, f.data))
      return Te(f), !0;
    if (!U[E] || w[E]) {
      if (!w[E] && Bn(E) && (v.tagNameCheck instanceof RegExp && J(v.tagNameCheck, E) || v.tagNameCheck instanceof Function && v.tagNameCheck(E)))
        return !1;
      if (Zt && !xe[E]) {
        const z = m(f) || f.parentNode, Z = h(f) || f.childNodes;
        if (Z && z) {
          const j = Z.length;
          for (let ee = j - 1; ee >= 0; --ee) {
            const Ce = k(Z[ee], !0);
            Ce.__removalCount = (f.__removalCount || 0) + 1, z.insertBefore(Ce, R(f));
          }
        }
      }
      return Te(f), !0;
    }
    return f instanceof s && !Tl(f) || (E === "noscript" || E === "noembed" || E === "noframes") && J(/<\/no(script|embed|frames)/i, f.innerHTML) ? (Te(f), !0) : (De && f.nodeType === Tt.text && (b = f.textContent, Pt([X, O, C], (z) => {
      b = wt(b, z, " ");
    }), f.textContent !== b && (bt(e.removed, {
      element: f.cloneNode()
    }), f.textContent = b)), Re(M.afterSanitizeElements, f, null), !1);
  }, Hn = function(f, b, E) {
    if ($n && (b === "id" || b === "name") && (E in t || E in Sl))
      return !1;
    if (!(dt && !B[b] && J(ae, b))) {
      if (!(de && J(ne, b))) {
        if (!G[b] || B[b]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(Bn(f) && (v.tagNameCheck instanceof RegExp && J(v.tagNameCheck, f) || v.tagNameCheck instanceof Function && v.tagNameCheck(f)) && (v.attributeNameCheck instanceof RegExp && J(v.attributeNameCheck, b) || v.attributeNameCheck instanceof Function && v.attributeNameCheck(b)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            b === "is" && v.allowCustomizedBuiltInElements && (v.tagNameCheck instanceof RegExp && J(v.tagNameCheck, E) || v.tagNameCheck instanceof Function && v.tagNameCheck(E)))
          ) return !1;
        } else if (!Kt[b]) {
          if (!J(ze, wt(E, je, ""))) {
            if (!((b === "src" || b === "xlink:href" || b === "href") && f !== "script" && Rs(E, "data:") === 0 && Rn[f])) {
              if (!(Ne && !J(Ue, wt(E, je, "")))) {
                if (E)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, Bn = function(f) {
    return f !== "annotation-xml" && Io(f, Xe);
  }, Gn = function(f) {
    Re(M.beforeSanitizeAttributes, f, null);
    const {
      attributes: b
    } = f;
    if (!b || en(f))
      return;
    const E = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: G,
      forceKeepAttr: void 0
    };
    let z = b.length;
    for (; z--; ) {
      const Z = b[z], {
        name: j,
        namespaceURI: ee,
        value: Ce
      } = Z, ht = V(j);
      let K = j === "value" ? Ce : Os(Ce);
      if (E.attrName = ht, E.attrValue = K, E.keepAttr = !0, E.forceKeepAttr = void 0, Re(M.uponSanitizeAttribute, f, E), K = E.attrValue, Ln && (ht === "id" || ht === "name") && (Nt(j, f), K = gl + K), mt && J(/((--!?|])>)|<\/(style|title)/i, K)) {
        Nt(j, f);
        continue;
      }
      if (E.forceKeepAttr || (Nt(j, f), !E.keepAttr))
        continue;
      if (!He && J(/\/>/i, K)) {
        Nt(j, f);
        continue;
      }
      De && Pt([X, O, C], (Vn) => {
        K = wt(K, Vn, " ");
      });
      const Wn = V(f.nodeName);
      if (Hn(Wn, ht, K)) {
        if (p && typeof g == "object" && typeof g.getAttributeType == "function" && !ee)
          switch (g.getAttributeType(Wn, ht)) {
            case "TrustedHTML": {
              K = p.createHTML(K);
              break;
            }
            case "TrustedScriptURL": {
              K = p.createScriptURL(K);
              break;
            }
          }
        try {
          ee ? f.setAttributeNS(ee, j, K) : f.setAttribute(j, K), en(f) ? Te(f) : Mo(e.removed);
        } catch {
        }
      }
    }
    Re(M.afterSanitizeAttributes, f, null);
  }, Cl = function A(f) {
    let b = null;
    const E = Fn(f);
    for (Re(M.beforeSanitizeShadowDOM, f, null); b = E.nextNode(); )
      Re(M.uponSanitizeShadowNode, b, null), zn(b), Gn(b), b.content instanceof i && A(b.content);
    Re(M.afterSanitizeShadowDOM, f, null);
  };
  return e.sanitize = function(A) {
    let f = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, b = null, E = null, z = null, Z = null;
    if (Jt = !A, Jt && (A = "<!-->"), typeof A != "string" && !Un(A))
      if (typeof A.toString == "function") {
        if (A = A.toString(), typeof A != "string")
          throw vt("dirty is not a string, aborting");
      } else
        throw vt("toString is not a function");
    if (!e.isSupported)
      return A;
    if (pe || xt(f), e.removed = [], typeof A == "string" && (pt = !1), pt) {
      if (A.nodeName) {
        const Ce = V(A.nodeName);
        if (!U[Ce] || w[Ce])
          throw vt("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (A instanceof r)
      b = Pn("<!---->"), E = b.ownerDocument.importNode(A, !0), E.nodeType === Tt.element && E.nodeName === "BODY" || E.nodeName === "HTML" ? b = E : b.appendChild(E);
    else {
      if (!Je && !De && !me && // eslint-disable-next-line unicorn/prefer-includes
      A.indexOf("<") === -1)
        return p && $t ? p.createHTML(A) : A;
      if (b = Pn(A), !b)
        return Je ? null : $t ? $ : "";
    }
    b && Be && Te(b.firstChild);
    const j = Fn(pt ? A : b);
    for (; z = j.nextNode(); )
      zn(z), Gn(z), z.content instanceof i && Cl(z.content);
    if (pt)
      return A;
    if (Je) {
      if (yt)
        for (Z = F.call(b.ownerDocument); b.firstChild; )
          Z.appendChild(b.firstChild);
      else
        Z = b;
      return (G.shadowroot || G.shadowrootmode) && (Z = Y.call(o, Z, !0)), Z;
    }
    let ee = me ? b.outerHTML : b.innerHTML;
    return me && U["!doctype"] && b.ownerDocument && b.ownerDocument.doctype && b.ownerDocument.doctype.name && J(ml, b.ownerDocument.doctype.name) && (ee = "<!DOCTYPE " + b.ownerDocument.doctype.name + `>
` + ee), De && Pt([X, O, C], (Ce) => {
      ee = wt(ee, Ce, " ");
    }), p && $t ? p.createHTML(ee) : ee;
  }, e.setConfig = function() {
    let A = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    xt(A), pe = !0;
  }, e.clearConfig = function() {
    tt = null, pe = !1;
  }, e.isValidAttribute = function(A, f, b) {
    tt || xt({});
    const E = V(A), z = V(f);
    return Hn(E, z, b);
  }, e.addHook = function(A, f) {
    typeof f == "function" && bt(M[A], f);
  }, e.removeHook = function(A, f) {
    if (f !== void 0) {
      const b = Ls(M[A], f);
      return b === -1 ? void 0 : qs(M[A], b, 1)[0];
    }
    return Mo(M[A]);
  }, e.removeHooks = function(A) {
    M[A] = [];
  }, e.removeAllHooks = function() {
    M = Bo();
  }, e;
}
pl();
const {
  SvelteComponent: ah,
  add_render_callback: sh,
  append: rh,
  attr: _h,
  bubble: fh,
  check_outros: ch,
  create_component: uh,
  create_in_transition: dh,
  create_out_transition: mh,
  destroy_component: ph,
  detach: gh,
  element: hh,
  group_outros: bh,
  init: wh,
  insert: vh,
  listen: Sh,
  mount_component: Th,
  run_all: Ch,
  safe_not_equal: Eh,
  set_data: kh,
  space: Ah,
  stop_propagation: yh,
  text: $h,
  toggle_class: Lh,
  transition_in: qh,
  transition_out: Rh
} = window.__gradio__svelte__internal, { createEventDispatcher: Oh, onMount: Nh } = window.__gradio__svelte__internal, {
  SvelteComponent: Dh,
  append: Mh,
  attr: Ih,
  bubble: Ph,
  check_outros: Fh,
  create_animation: Uh,
  create_component: zh,
  destroy_component: Hh,
  detach: Bh,
  element: Gh,
  ensure_array_like: Wh,
  fix_and_outro_and_destroy_block: Vh,
  fix_position: Yh,
  group_outros: jh,
  init: Xh,
  insert: Zh,
  mount_component: Kh,
  noop: Jh,
  safe_not_equal: Qh,
  set_style: xh,
  space: eb,
  transition_in: tb,
  transition_out: nb,
  update_keyed_each: ob
} = window.__gradio__svelte__internal, {
  SvelteComponent: js,
  add_flush_callback: Go,
  assign: Xs,
  bind: Wo,
  binding_callbacks: Vo,
  create_component: Cn,
  destroy_component: En,
  detach: Zs,
  get_spread_object: Ks,
  get_spread_update: Js,
  init: Qs,
  insert: xs,
  mount_component: kn,
  safe_not_equal: er,
  space: tr,
  transition_in: An,
  transition_out: yn
} = window.__gradio__svelte__internal;
function nr(n) {
  let e, t, o, l, i, a;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        n[16].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[16].i18n
    ) },
    /*loading_status*/
    n[14]
  ];
  let s = {};
  for (let u = 0; u < r.length; u += 1)
    s = Xs(s, r[u]);
  e = new ks({ props: s }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[18]
  );
  function _(u) {
    n[19](u);
  }
  function c(u) {
    n[20](u);
  }
  let d = {
    choices: (
      /*choices*/
      n[8]
    ),
    max_choices: (
      /*max_choices*/
      n[7]
    ),
    label: (
      /*label*/
      n[2]
    ),
    info: (
      /*info*/
      n[3]
    ),
    show_label: (
      /*show_label*/
      n[9]
    ),
    allow_custom_value: (
      /*allow_custom_value*/
      n[15]
    ),
    filterable: (
      /*filterable*/
      n[10]
    ),
    container: (
      /*container*/
      n[11]
    ),
    i18n: (
      /*gradio*/
      n[16].i18n
    ),
    disabled: !/*interactive*/
    n[17]
  };
  return (
    /*value*/
    n[0] !== void 0 && (d.value = /*value*/
    n[0]), /*value_is_output*/
    n[1] !== void 0 && (d.value_is_output = /*value_is_output*/
    n[1]), o = new Ya({ props: d }), Vo.push(() => Wo(o, "value", _)), Vo.push(() => Wo(o, "value_is_output", c)), o.$on(
      "change",
      /*change_handler*/
      n[21]
    ), o.$on(
      "input",
      /*input_handler*/
      n[22]
    ), o.$on(
      "select",
      /*select_handler*/
      n[23]
    ), o.$on(
      "blur",
      /*blur_handler*/
      n[24]
    ), o.$on(
      "focus",
      /*focus_handler*/
      n[25]
    ), o.$on(
      "key_up",
      /*key_up_handler*/
      n[26]
    ), {
      c() {
        Cn(e.$$.fragment), t = tr(), Cn(o.$$.fragment);
      },
      m(u, g) {
        kn(e, u, g), xs(u, t, g), kn(o, u, g), a = !0;
      },
      p(u, g) {
        const T = g & /*gradio, loading_status*/
        81920 ? Js(r, [
          g & /*gradio*/
          65536 && {
            autoscroll: (
              /*gradio*/
              u[16].autoscroll
            )
          },
          g & /*gradio*/
          65536 && { i18n: (
            /*gradio*/
            u[16].i18n
          ) },
          g & /*loading_status*/
          16384 && Ks(
            /*loading_status*/
            u[14]
          )
        ]) : {};
        e.$set(T);
        const k = {};
        g & /*choices*/
        256 && (k.choices = /*choices*/
        u[8]), g & /*max_choices*/
        128 && (k.max_choices = /*max_choices*/
        u[7]), g & /*label*/
        4 && (k.label = /*label*/
        u[2]), g & /*info*/
        8 && (k.info = /*info*/
        u[3]), g & /*show_label*/
        512 && (k.show_label = /*show_label*/
        u[9]), g & /*allow_custom_value*/
        32768 && (k.allow_custom_value = /*allow_custom_value*/
        u[15]), g & /*filterable*/
        1024 && (k.filterable = /*filterable*/
        u[10]), g & /*container*/
        2048 && (k.container = /*container*/
        u[11]), g & /*gradio*/
        65536 && (k.i18n = /*gradio*/
        u[16].i18n), g & /*interactive*/
        131072 && (k.disabled = !/*interactive*/
        u[17]), !l && g & /*value*/
        1 && (l = !0, k.value = /*value*/
        u[0], Go(() => l = !1)), !i && g & /*value_is_output*/
        2 && (i = !0, k.value_is_output = /*value_is_output*/
        u[1], Go(() => i = !1)), o.$set(k);
      },
      i(u) {
        a || (An(e.$$.fragment, u), An(o.$$.fragment, u), a = !0);
      },
      o(u) {
        yn(e.$$.fragment, u), yn(o.$$.fragment, u), a = !1;
      },
      d(u) {
        u && Zs(t), En(e, u), En(o, u);
      }
    }
  );
}
function or(n) {
  let e, t;
  return e = new Ul({
    props: {
      visible: (
        /*visible*/
        n[6]
      ),
      elem_id: (
        /*elem_id*/
        n[4]
      ),
      elem_classes: (
        /*elem_classes*/
        n[5]
      ),
      padding: (
        /*container*/
        n[11]
      ),
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[12]
      ),
      min_width: (
        /*min_width*/
        n[13]
      ),
      $$slots: { default: [nr] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Cn(e.$$.fragment);
    },
    m(o, l) {
      kn(e, o, l), t = !0;
    },
    p(o, [l]) {
      const i = {};
      l & /*visible*/
      64 && (i.visible = /*visible*/
      o[6]), l & /*elem_id*/
      16 && (i.elem_id = /*elem_id*/
      o[4]), l & /*elem_classes*/
      32 && (i.elem_classes = /*elem_classes*/
      o[5]), l & /*container*/
      2048 && (i.padding = /*container*/
      o[11]), l & /*scale*/
      4096 && (i.scale = /*scale*/
      o[12]), l & /*min_width*/
      8192 && (i.min_width = /*min_width*/
      o[13]), l & /*$$scope, choices, max_choices, label, info, show_label, allow_custom_value, filterable, container, gradio, interactive, value, value_is_output, loading_status*/
      134467471 && (i.$$scope = { dirty: l, ctx: o }), e.$set(i);
    },
    i(o) {
      t || (An(e.$$.fragment, o), t = !0);
    },
    o(o) {
      yn(e.$$.fragment, o), t = !1;
    },
    d(o) {
      En(e, o);
    }
  };
}
function lr(n, e, t) {
  let { label: o = "Dropdown" } = e, { info: l = void 0 } = e, { elem_id: i = "" } = e, { elem_classes: a = [] } = e, { visible: r = !0 } = e, { value: s = void 0 } = e, { value_is_output: _ = !1 } = e, { max_choices: c = null } = e, { choices: d } = e, { show_label: u } = e, { filterable: g } = e, { container: T = !0 } = e, { scale: k = null } = e, { min_width: y = void 0 } = e, { loading_status: R } = e, { allow_custom_value: h = !1 } = e, { gradio: m } = e, { interactive: p } = e;
  const $ = () => m.dispatch("clear_status", R);
  function S(C) {
    s = C, t(0, s);
  }
  function D(C) {
    _ = C, t(1, _);
  }
  const F = () => m.dispatch("change"), P = () => m.dispatch("input"), Y = (C) => m.dispatch("select", C.detail), M = () => m.dispatch("blur"), X = () => m.dispatch("focus"), O = () => m.dispatch("key_up");
  return n.$$set = (C) => {
    "label" in C && t(2, o = C.label), "info" in C && t(3, l = C.info), "elem_id" in C && t(4, i = C.elem_id), "elem_classes" in C && t(5, a = C.elem_classes), "visible" in C && t(6, r = C.visible), "value" in C && t(0, s = C.value), "value_is_output" in C && t(1, _ = C.value_is_output), "max_choices" in C && t(7, c = C.max_choices), "choices" in C && t(8, d = C.choices), "show_label" in C && t(9, u = C.show_label), "filterable" in C && t(10, g = C.filterable), "container" in C && t(11, T = C.container), "scale" in C && t(12, k = C.scale), "min_width" in C && t(13, y = C.min_width), "loading_status" in C && t(14, R = C.loading_status), "allow_custom_value" in C && t(15, h = C.allow_custom_value), "gradio" in C && t(16, m = C.gradio), "interactive" in C && t(17, p = C.interactive);
  }, [
    s,
    _,
    o,
    l,
    i,
    a,
    r,
    c,
    d,
    u,
    g,
    T,
    k,
    y,
    R,
    h,
    m,
    p,
    $,
    S,
    D,
    F,
    P,
    Y,
    M,
    X,
    O
  ];
}
class lb extends js {
  constructor(e) {
    super(), Qs(this, e, lr, or, er, {
      label: 2,
      info: 3,
      elem_id: 4,
      elem_classes: 5,
      visible: 6,
      value: 0,
      value_is_output: 1,
      max_choices: 7,
      choices: 8,
      show_label: 9,
      filterable: 10,
      container: 11,
      scale: 12,
      min_width: 13,
      loading_status: 14,
      allow_custom_value: 15,
      gradio: 16,
      interactive: 17
    });
  }
}
export {
  Ya as BaseMultiselect,
  lb as default
};

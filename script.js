/* ==========================================================================
   RISHTA TRUST — MAIN SCRIPT (v4.0)
   No dependencies. Every feature is guarded, so this one file serves all pages.
   ========================================================================== */

'use strict';

(() => {
  // --------------------------------------------------------------------------
  // 1. CONFIG — published office contacts, embedded by the build from src/data/site.json
  // --------------------------------------------------------------------------
  let CONFIG = { offices: {}, defaultOffice: 'faisalabad', fee: '' };
  try {
    CONFIG = JSON.parse(document.getElementById('site-config')?.textContent || '{}');
  } catch {
    /* keep defaults; forms will show a contact fallback */
  }
  const officeFor = (id) => CONFIG.offices?.[id] || CONFIG.offices?.[CONFIG.defaultOffice];

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const behavior = () => (prefersReducedMotion.matches ? 'auto' : 'smooth');

  // --------------------------------------------------------------------------
  // 2. UTILITIES
  // --------------------------------------------------------------------------
  const Utils = {
    whatsAppUrl(phone, message) {
      return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    },
    mailtoUrl(email, subject, body) {
      return `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    },
    icon(id) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'icon');
      svg.setAttribute('aria-hidden', 'true');
      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttribute('href', `#${id}`);
      svg.appendChild(use);
      return svg;
    },
    lockScroll(lock) {
      document.documentElement.classList.toggle('scroll-locked', lock);
    }
  };

  // --------------------------------------------------------------------------
  // 3. HEADER STATE + BACK TO TOP
  // --------------------------------------------------------------------------
  const header = $('#header');
  const backToTop = $('#backToTop');
  let scrollTicking = false;

  const onScroll = () => {
    const y = window.scrollY;
    header?.classList.toggle('is-scrolled', y > 8);
    backToTop?.classList.toggle('is-visible', y > 600);
    scrollTicking = false;
  };
  window.addEventListener('scroll', () => {
    if (!scrollTicking) { scrollTicking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  backToTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: behavior() });
    const target = $('#main') || document.body;
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  });

  // --------------------------------------------------------------------------
  // 4. MOBILE NAVIGATION
  // --------------------------------------------------------------------------
  const navToggle = $('#navToggle');
  const mobileNav = $('#mobileNav');

  const Nav = {
    isOpen: () => header?.classList.contains('is-open') ?? false,
    open() {
      header.classList.add('is-open');
      navToggle.setAttribute('aria-expanded', 'true');
      navToggle.setAttribute('aria-label', 'Close menu');
      Utils.lockScroll(true);
    },
    close({ returnFocus = false } = {}) {
      if (!Nav.isOpen()) return;
      header.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-label', 'Open menu');
      Utils.lockScroll(false);
      if (returnFocus) navToggle.focus();
    }
  };

  if (navToggle && mobileNav && header) {
    navToggle.addEventListener('click', () => (Nav.isOpen() ? Nav.close() : Nav.open()));
    mobileNav.addEventListener('click', (e) => {
      if (e.target.closest('a, [data-open-modal]')) Nav.close();
    });
    document.addEventListener('click', (e) => {
      if (Nav.isOpen() && !header.contains(e.target)) Nav.close();
    });
    window.matchMedia('(min-width: 1081px)').addEventListener('change', (e) => { if (e.matches) Nav.close(); });
  }

  // --------------------------------------------------------------------------
  // 5. SCROLL REVEAL (runs once per element)
  // --------------------------------------------------------------------------
  $$('[data-reveal-stagger]').forEach((group) => {
    $$(':scope > .reveal', group).forEach((child, i) => {
      child.style.setProperty('--reveal-delay', `${Math.min(i, 5) * 90}ms`);
    });
  });

  const revealTargets = $$('.reveal, [data-steps]');
  if ('IntersectionObserver' in window && !prefersReducedMotion.matches) {
    document.documentElement.classList.add('reveal-ready');
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealTargets.forEach((el) => observer.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add('is-visible'));
  }

  // --------------------------------------------------------------------------
  // 5b. DEPTH — pointer-driven 3D tilt. Writes CSS variables only (CSS does the transform),
  //     at most once per animation frame, on fine pointers without reduced motion.
  // --------------------------------------------------------------------------
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

  const attachTilt = (surface, target, { maxDeg, xVar, yVar, activeClass }) => {
    let frame = 0;
    let px = 0;
    let py = 0;
    const apply = () => {
      frame = 0;
      target.style.setProperty(yVar, `${(px * 2 * maxDeg).toFixed(2)}deg`);
      target.style.setProperty(xVar, `${(-py * 2 * maxDeg).toFixed(2)}deg`);
    };
    surface.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse' || prefersReducedMotion.matches) return;
      const r = surface.getBoundingClientRect();
      px = (e.clientX - r.left) / r.width - 0.5;   // -0.5 … 0.5
      py = (e.clientY - r.top) / r.height - 0.5;
      if (activeClass) target.classList.add(activeClass);
      if (!frame) frame = requestAnimationFrame(apply);
    });
    surface.addEventListener('pointerleave', () => {
      if (frame) { cancelAnimationFrame(frame); frame = 0; }
      if (activeClass) target.classList.remove(activeClass);
      target.style.setProperty(xVar, '0deg');
      target.style.setProperty(yVar, '0deg');
    });
  };

  if (finePointer.matches && !prefersReducedMotion.matches) {
    const heroStage = $('[data-hero-stage]');
    const heroSection = heroStage?.closest('.hero');
    if (heroStage && heroSection) {
      attachTilt(heroSection, heroStage, { maxDeg: 3, xVar: '--rx', yVar: '--ry', activeClass: 'is-tilting' });
    }
    $$('.proposal, .benefit, .news-card, .fee-panel').forEach((card) => {
      // Gentler on wide cards and on the fee panel, so the price stays calm and readable
      const wide = card.getBoundingClientRect().width > 700;
      const maxDeg = card.classList.contains('fee-panel') ? 2 : wide ? 1.2 : 3;
      attachTilt(card, card, { maxDeg, xVar: '--tx', yVar: '--ty' });
    });
  }

  // --------------------------------------------------------------------------
  // 6. MODALS — focus moved in, trapped, and restored; ESC / backdrop to close
  // --------------------------------------------------------------------------
  const Modal = {
    active: null,
    returnFocus: null,

    open(id, { returnFocusTo } = {}) {
      const modal = document.getElementById(id);
      if (!modal) return;
      if (Modal.active) Modal.close({ restoreFocus: false });
      Help.close();
      Nav.close();

      Modal.returnFocus = returnFocusTo || document.activeElement;
      Modal.active = modal;
      modal.classList.add('is-open');
      Utils.lockScroll(true);
      Array.from(document.body.children).forEach((el) => {
        if (el !== modal && el.tagName !== 'SCRIPT') el.inert = true;
      });

      const firstAction = $('.modal__actions a[href], .modal__actions button', modal) || $(FOCUSABLE, modal);
      requestAnimationFrame(() => firstAction?.focus());
    },

    close({ restoreFocus = true } = {}) {
      const modal = Modal.active;
      if (!modal) return;
      modal.classList.remove('is-open');
      Array.from(document.body.children).forEach((el) => { el.inert = false; });
      Utils.lockScroll(false);
      Modal.active = null;
      if (restoreFocus && Modal.returnFocus?.isConnected) Modal.returnFocus.focus({ preventScroll: true });
    },

    trapTab(e) {
      const focusables = $$(FOCUSABLE, Modal.active).filter((el) => el.offsetParent !== null);
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  };

  $$('.modal').forEach((modal) => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal || e.target.closest('[data-modal-close]')) Modal.close();
    });
  });

  // --------------------------------------------------------------------------
  // 7. HELP WIDGET
  // --------------------------------------------------------------------------
  const helpToggle = $('#helpToggle');
  const helpPopover = $('#helpPopover');

  const Help = {
    isOpen: () => helpPopover?.classList.contains('is-open') ?? false,
    open() {
      if (!helpPopover) return;
      Nav.close();
      helpPopover.classList.add('is-open');
      helpToggle.setAttribute('aria-expanded', 'true');
      requestAnimationFrame(() => $('.help-item', helpPopover)?.focus());
    },
    close({ returnFocus = false } = {}) {
      if (!Help.isOpen()) return;
      helpPopover.classList.remove('is-open');
      helpToggle.setAttribute('aria-expanded', 'false');
      if (returnFocus) helpToggle.focus();
    }
  };

  if (helpToggle && helpPopover) {
    helpToggle.addEventListener('click', () => (Help.isOpen() ? Help.close() : Help.open()));
    helpPopover.addEventListener('click', (e) => {
      const item = e.target.closest('[data-help-close]');
      if (item && !item.hasAttribute('data-open-modal')) Help.close();
    });
    document.addEventListener('click', (e) => {
      if (e.target.closest('[data-open-help]')) { e.preventDefault(); Help.open(); return; }
      if (Help.isOpen() && !helpPopover.contains(e.target) && !helpToggle.contains(e.target)) Help.close();
    });
    helpPopover.addEventListener('focusout', (e) => {
      if (e.relatedTarget && !helpPopover.contains(e.relatedTarget) && e.relatedTarget !== helpToggle) Help.close();
    });
  }

  // Any element with data-open-modal="id" opens that modal
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-open-modal]');
    if (!trigger) return;
    e.preventDefault();
    const fromHelp = helpPopover?.contains(trigger);
    Modal.open(trigger.dataset.openModal, { returnFocusTo: fromHelp ? helpToggle : trigger });
  });

  // --------------------------------------------------------------------------
  // 8. GLOBAL KEYBOARD — ESC closes the top-most layer; Tab is trapped in modals
  // --------------------------------------------------------------------------
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (Modal.active) { Modal.close(); return; }
      if (Help.isOpen()) { Help.close({ returnFocus: true }); return; }
      if (Nav.isOpen()) { Nav.close({ returnFocus: true }); return; }
    }
    if (e.key === 'Tab' && Modal.active) Modal.trapTab(e);
  });

  // --------------------------------------------------------------------------
  // 9. FORM VALIDATION
  // --------------------------------------------------------------------------
  const Validate = {
    rules: {
      phone(value) {
        const digits = value.replace(/\D/g, '');
        if (!value.trim()) return 'Please enter a mobile or WhatsApp number.';
        if (!/^[+\d\s()-]+$/.test(value.trim()) || digits.length < 10 || digits.length > 15) {
          return 'Please enter a valid number, e.g. 0323-1234567 or +44 7700 900123.';
        }
        return '';
      },
      text(value, field) {
        if (value.trim().length < 2) return `Please enter ${field.dataset.label || 'this field'}.`;
        return '';
      },
      select(value, field) {
        return value ? '' : `Please choose ${field.dataset.label || 'an option'}.`;
      },
      age(value) {
        const n = Number(value);
        if (!value.trim()) return 'Please enter the age.';
        if (!Number.isInteger(n) || n < 18 || n > 70) return 'Age must be a whole number between 18 and 70.';
        return '';
      },
      email(value) {
        if (!value.trim()) return ''; // optional
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value.trim()) ? '' : 'Please enter a valid email address, or leave it blank.';
      },
      consent(_value, field) {
        return field.checked ? '' : 'Please confirm you agree before continuing.';
      }
    },

    field(input) {
      const rule = Validate.rules[input.dataset.rule];
      if (!rule) return true;
      const message = rule(input.value, input);
      const errorEl = document.getElementById(`${input.id}-error`);
      input.setAttribute('aria-invalid', message ? 'true' : 'false');
      input.classList.toggle('is-valid', !message && input.type !== 'checkbox' && input.value.trim() !== '');
      if (errorEl) errorEl.textContent = message;
      return !message;
    },

    group(container) {
      const invalid = $$('[data-rule]', container).filter((input) => !Validate.field(input));
      if (invalid.length) invalid[0].focus();
      return invalid.length === 0;
    },

    attach(rules) {
      Object.entries(rules).forEach(([id, [rule, label]]) => {
        const input = document.getElementById(id);
        if (!input) return;
        input.dataset.rule = rule;
        if (label) input.dataset.label = label;
        const revalidate = () => { if (input.getAttribute('aria-invalid') === 'true') Validate.field(input); };
        input.addEventListener('blur', () => { if (input.value && input.type !== 'checkbox') Validate.field(input); });
        input.addEventListener('input', revalidate);
        input.addEventListener('change', revalidate);
      });
    }
  };

  // --------------------------------------------------------------------------
  // 10. WHATSAPP HAND-OFF (nothing is stored; the user reviews and sends in WhatsApp)
  // --------------------------------------------------------------------------
  const showHandoff = (office, message, { emailSubject } = {}) => {
    const container = $('#waButtonContainer');
    if (!container || !office) return;
    const link = document.createElement('a');
    link.className = 'btn btn-whatsapp btn-lg btn-block';
    link.href = Utils.whatsAppUrl(office.wa, message);
    link.target = '_blank';
    link.rel = 'noopener';
    link.append(Utils.icon('i-whatsapp'), document.createTextNode(` Open WhatsApp — ${office.name}`));
    const items = [link];

    if (emailSubject && office.email) {
      const mail = document.createElement('a');
      mail.className = 'btn btn-secondary btn-block';
      mail.href = Utils.mailtoUrl(office.email, emailSubject, message);
      mail.append(Utils.icon('i-mail'), document.createTextNode(' Send by email instead'));
      items.push(mail);
    }

    const close = document.createElement('button');
    close.type = 'button';
    close.className = 'btn btn-secondary btn-block';
    close.setAttribute('data-modal-close', '');
    close.textContent = 'Close';
    items.push(close);

    container.replaceChildren(...items);
    Modal.open('confirmationModal');
  };

  // --------------------------------------------------------------------------
  // 11. REGISTRATION (5 steps; the last step hands the details to a consultant)
  // --------------------------------------------------------------------------
  const regForm = $('#registrationForm');
  if (regForm) {
    const steps = $$('.reg-step', regForm);
    const indicators = $$('[data-step-indicator]');
    const card = $('#register');
    const done = $('#regDone');
    const summary = $('#regSummary');
    let current = 1;

    Validate.attach({
      regName: ['text', 'the candidate’s full name'],
      regFor: ['select', 'who you are registering'],
      regGender: ['select', 'the candidate’s gender'],
      regAge: ['age'],
      regStatus: ['select', 'a marital status'],
      regCity: ['text', 'a city or country'],
      regPhone: ['phone'],
      regEmail: ['email'],
      regEducation: ['text', 'the candidate’s education'],
      regProfession: ['text', 'the candidate’s profession'],
      regConsent: ['consent']
    });

    const show = (n, { focus = true } = {}) => {
      current = n;
      steps.forEach((s) => s.classList.toggle('is-active', Number(s.dataset.step) === n));
      indicators.forEach((li) => {
        const i = Number(li.dataset.stepIndicator);
        li.classList.toggle('is-done', i < n);
        if (i === n) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current');
      });
      if (!focus) return;
      if (card.getBoundingClientRect().top < 0) card.scrollIntoView({ block: 'start', behavior: behavior() });
      const title = n === 5 ? $('.reg-step__title', done) : $('.reg-step__title', steps[n - 1]);
      title?.focus({ preventScroll: true });
    };

    const value = (id) => document.getElementById(id)?.value.trim() || '';
    const officeSelect = $('#regOffice');

    const FIELDS = [
      ['regName', 'Candidate'], ['regFor', 'Registering for'], ['regGender', 'Gender'], ['regAge', 'Age'],
      ['regStatus', 'Marital status'], ['regCity', 'Lives in'], ['regPhone', 'Phone / WhatsApp'], ['regEmail', 'Email'],
      ['regOffice', 'Consultant'], ['regEducation', 'Education'], ['regProfession', 'Profession'], ['regAbout', 'About', true]
    ];
    const display = (id) => (id === 'regOffice' ? officeSelect.selectedOptions[0]?.textContent.trim() : value(id)) || 'Not provided';

    const buildSummary = () => {
      const rows = FIELDS.map(([id, label, wide]) => {
        const row = document.createElement('div');
        if (wide) row.className = 'summary__wide';
        const dt = document.createElement('dt');
        dt.textContent = label;
        const dd = document.createElement('dd');
        dd.textContent = display(id);
        row.append(dt, dd);
        return row;
      });
      summary.replaceChildren(...rows);
    };

    const buildMessage = (office) => [
      `Assalam-o-Alaikum ${office.name},`,
      '',
      `I would like to register with Rishta Trust (one-time registration fee ${CONFIG.fee}).`,
      '',
      ...FIELDS.filter(([id]) => id !== 'regOffice').map(([id, label]) => `• ${label}: ${display(id)}`),
      '',
      'I agree to the Terms & Conditions and Privacy Policy. Please confirm my details and the next steps.'
    ].join('\n');

    regForm.classList.add('js-steps');
    show(1, { focus: false });

    regForm.addEventListener('click', (e) => {
      if (e.target.closest('[data-step-next]')) {
        if (!Validate.group(steps[current - 1])) return;
        if (current === 3) buildSummary();
        show(current + 1);
      } else if (e.target.closest('[data-step-back]')) {
        show(current - 1);
      }
    });

    regForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Enter inside an earlier step means "continue", not "submit"
      if (current < 4) { $('[data-step-next]', steps[current - 1])?.click(); return; }
      if (!Validate.group(steps[3])) return;

      const office = officeFor(officeSelect.value);
      const waLink = $('#regWhatsApp');
      if (!office || !waLink) return;
      waLink.href = Utils.whatsAppUrl(office.wa, buildMessage(office));
      $('#regWhatsAppLabel').textContent = `Open WhatsApp — ${office.name}`;
      regForm.hidden = true;
      done.hidden = false;
      show(5);
    });

    $('#regRestart')?.addEventListener('click', () => {
      done.hidden = true;
      regForm.hidden = false;
      show(1);
    });
  }

  // --------------------------------------------------------------------------
  // 12. CONTACT FORM
  // --------------------------------------------------------------------------
  const contactForm = $('#contactForm');
  if (contactForm) {
    Validate.attach({
      cName: ['text', 'your name'],
      cPhone: ['phone'],
      cEmail: ['email'],
      cMessage: ['text', 'a message']
    });
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!Validate.group(contactForm)) return;
      const office = officeFor($('#cOffice').value);
      const v = (id) => $(`#${id}`).value.trim();
      const message = [
        `Assalam-o-Alaikum ${office.name},`,
        '',
        v('cMessage'),
        '',
        `— ${v('cName')}`,
        `Phone: ${v('cPhone')}`,
        v('cEmail') ? `Email: ${v('cEmail')}` : ''
      ].filter((line, i, arr) => line !== '' || arr[i - 1] !== '').join('\n').trim();
      showHandoff(office, message, { emailSubject: `Website enquiry from ${v('cName')}` });
    });
  }

  // --------------------------------------------------------------------------
  // 13. MATCH FILTERS (matches.html)
  // --------------------------------------------------------------------------
  const matchFilters = $('#matchFilters');
  if (matchFilters) {
    const cards = $$('#matchGrid .proposal');
    const count = $('#matchCount');
    const empty = $('#matchEmpty');

    const apply = () => {
      const gender = $('#fGender').value;
      const min = Number($('#fAgeMin').value) || 0;
      const max = Number($('#fAgeMax').value) || 999;
      const terms = $('#fSearch').value.toLowerCase().split(/\s+/).filter(Boolean);
      let shown = 0;
      cards.forEach((card) => {
        const age = Number(card.dataset.age);
        const match = (!gender || card.dataset.gender === gender) && age >= min && age <= max &&
          terms.every((t) => card.dataset.search.includes(t));
        card.hidden = !match;
        if (match) shown += 1;
      });
      empty.hidden = shown > 0;
      count.textContent = `Showing ${shown} of ${cards.length} sample listings`;
    };

    matchFilters.addEventListener('input', apply);
    matchFilters.addEventListener('change', apply);
    matchFilters.addEventListener('submit', (e) => e.preventDefault());
    matchFilters.addEventListener('reset', () => requestAnimationFrame(apply));
    $('[data-match-reset]')?.addEventListener('click', () => { matchFilters.reset(); $('#fGender').focus(); });
    apply();
  }

  // --------------------------------------------------------------------------
  // 14. NEWS FILTER (news.html)
  // --------------------------------------------------------------------------
  const filterBar = $('[data-news-filter]');
  if (filterBar) {
    const cards = $$('.news-grid--page [data-category]');
    const empty = $('#newsEmpty');
    const status = $('#newsStatus');
    filterBar.addEventListener('click', (e) => {
      const chip = e.target.closest('[data-filter]');
      if (!chip) return;
      const filter = chip.dataset.filter;
      $$('[data-filter]', filterBar).forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
      let shown = 0;
      cards.forEach((card) => {
        const match = filter === 'all' || card.dataset.category === filter;
        card.hidden = !match;
        if (match) shown += 1;
      });
      if (empty) empty.hidden = shown > 0;
      if (status) status.textContent = `${shown} article${shown === 1 ? '' : 's'} shown`;
    });
    $('[data-filter-reset]')?.addEventListener('click', () => $('[data-filter="all"]', filterBar)?.click());
  }

  // --------------------------------------------------------------------------
  // 15. SHARE (article pages)
  // --------------------------------------------------------------------------
  const shareStatus = $('#shareStatus');
  $('[data-share-copy]')?.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      if (shareStatus) shareStatus.textContent = 'Link copied.';
    } catch {
      if (shareStatus) shareStatus.textContent = 'Copy failed — please copy the address bar link.';
    }
  });
  const nativeShare = $('[data-share-native]');
  if (nativeShare && navigator.share) {
    nativeShare.hidden = false;
    nativeShare.addEventListener('click', () => {
      navigator.share({ title: document.title, url: window.location.href }).catch(() => {});
    });
  }
  $$('[data-share-whatsapp]').forEach((a) => {
    a.href = `https://wa.me/?text=${encodeURIComponent(`${document.title} — ${window.location.href}`)}`;
  });
})();

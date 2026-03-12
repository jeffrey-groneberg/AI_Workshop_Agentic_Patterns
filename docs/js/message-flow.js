/**
 * Interactive Message Flow — step-through visualisation for the workshop.
 *
 * Each widget is a <div class="message-flow-interactive"> containing
 * <div class="mf-step"> children, each with <div class="mf-msg"> children.
 * The JS reads data-* attributes, builds a cumulative message stack, and
 * renders a navigable step-by-step UI. Supports multiple parallel message
 * lists (for concurrent / sequential patterns) via the data-list attribute.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.message-flow-interactive').forEach(initFlow);
  });

  /* ── Initialise one flow widget ───────────────────── */
  function initFlow(container) {
    var stepEls = container.querySelectorAll(':scope > .mf-step');
    if (!stepEls.length) return;

    /* --- Parse data from HTML ------------------------------------ */
    var title       = container.getAttribute('data-title') || 'Message Flow';
    var ctxType     = container.getAttribute('data-context-type') || 'isolated';
    var ctxLabel    = container.getAttribute('data-context-label') || '';

    var steps = [];
    var listNamesSet = {};

    stepEls.forEach(function (stepEl) {
      var desc = stepEl.getAttribute('data-description') || '';
      var msgs = [];
      stepEl.querySelectorAll(':scope > .mf-msg').forEach(function (msgEl) {
        var listName = msgEl.getAttribute('data-list') || 'messages';
        listNamesSet[listName] = true;
        msgs.push({
          role:    msgEl.getAttribute('data-role') || 'user',
          agent:   msgEl.getAttribute('data-agent') || '',
          content: msgEl.textContent.trim(),
          list:    listName,
          payload: msgEl.getAttribute('data-payload') || ''
        });
      });
      steps.push({ description: desc, messages: msgs });
    });

    var listNames = Object.keys(listNamesSet);
    var totalSteps = steps.length;
    var state = { step: 0 };

    /* --- Build UI ------------------------------------------------ */
    container.innerHTML = ''; // remove source step divs

    var wrapper = el('div', 'mf-wrapper');

    // Header
    var header = el('div', 'mf-header');
    var badge  = el('span', 'mf-badge mf-badge--' + ctxType);
    badge.textContent = ctxLabel;
    var titleEl = el('span', 'mf-title');
    titleEl.textContent = title;
    header.appendChild(badge);
    header.appendChild(titleEl);

    // Description
    var desc = el('div', 'mf-description');

    // Controls
    var controls = el('div', 'mf-controls');
    var prevBtn  = el('button', 'mf-btn mf-btn--prev');
    prevBtn.textContent = '\u2190 Previous';
    prevBtn.disabled = true;
    var counter = el('span', 'mf-counter');
    var nextBtn = el('button', 'mf-btn mf-btn--next');
    nextBtn.textContent = 'Next \u2192';
    controls.appendChild(prevBtn);
    controls.appendChild(counter);
    controls.appendChild(nextBtn);

    // Stack area
    var stackArea = el('div', 'mf-stack-area');

    wrapper.appendChild(header);
    wrapper.appendChild(desc);
    wrapper.appendChild(controls);
    wrapper.appendChild(stackArea);
    container.appendChild(wrapper);

    /* --- Event handlers ------------------------------------------ */
    prevBtn.addEventListener('click', function () {
      if (state.step > 0) { state.step--; render(); }
    });
    nextBtn.addEventListener('click', function () {
      if (state.step < totalSteps - 1) { state.step++; render(); }
    });

    // Keyboard navigation when container or its children have focus
    container.setAttribute('tabindex', '0');
    container.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        if (state.step < totalSteps - 1) { state.step++; render(); }
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (state.step > 0) { state.step--; render(); }
      }
    });

    /* --- Render -------------------------------------------------- */
    function render() {
      prevBtn.disabled = state.step === 0;
      nextBtn.disabled = state.step === totalSteps - 1;
      counter.textContent = 'Step ' + (state.step + 1) + ' of ' + totalSteps;
      desc.textContent = steps[state.step].description;

      // Accumulate messages per list up to current step
      var lists = {};
      listNames.forEach(function (n) { lists[n] = []; });

      for (var i = 0; i <= state.step; i++) {
        steps[i].messages.forEach(function (m) {
          lists[m.list].push({
            role:    m.role,
            agent:   m.agent,
            content: m.content,
            payload: m.payload,
            isNew:   i === state.step
          });
        });
      }

      // Render columns
      stackArea.innerHTML = '';
      var isSingle = listNames.length === 1;
      stackArea.className = 'mf-stack-area ' +
        (isSingle ? 'mf-stack-area--single' : 'mf-stack-area--multi');

      listNames.forEach(function (listName) {
        var col = el('div', 'mf-list-col');

        if (!isSingle) {
          var colHeader = el('div', 'mf-list-header');
          colHeader.textContent = listName;
          col.appendChild(colHeader);
        }

        var msgContainer = el('div', 'mf-messages');
        var msgs = lists[listName];

        msgs.forEach(function (m) {
          var card = el('div', 'mf-card mf-card--' + m.role + (m.isNew ? ' mf-card--new' : ''));

          var cardHeader = el('div', 'mf-card-header');
          var roleLabel  = el('span', 'mf-role');
          roleLabel.textContent = m.role;
          var agentLabel = el('span', 'mf-agent');
          agentLabel.textContent = m.agent;
          cardHeader.appendChild(roleLabel);
          cardHeader.appendChild(agentLabel);

          var content = el('div', 'mf-content');
          content.textContent = m.content;

          card.appendChild(cardHeader);
          card.appendChild(content);

          // Collapsible API payload
          if (m.payload) {
            var toggleBtn = el('button', 'mf-payload-toggle');
            toggleBtn.textContent = '{ } Show API Payload';
            toggleBtn.addEventListener('click', function () {
              var block = this.nextElementSibling;
              if (block.style.display === 'none') {
                block.style.display = 'block';
                this.textContent = '{ } Hide API Payload';
                this.classList.add('mf-payload-toggle--active');
              } else {
                block.style.display = 'none';
                this.textContent = '{ } Show API Payload';
                this.classList.remove('mf-payload-toggle--active');
              }
            });

            var payloadBlock = el('pre', 'mf-payload-block');
            payloadBlock.style.display = 'none';
            var payloadCode = el('code', 'mf-payload-code');
            try {
              payloadCode.textContent = JSON.stringify(JSON.parse(m.payload), null, 2);
            } catch (e) {
              payloadCode.textContent = m.payload;
            }
            payloadBlock.appendChild(payloadCode);
            card.appendChild(toggleBtn);
            card.appendChild(payloadBlock);
          }

          msgContainer.appendChild(card);
        });

        // Message count
        if (msgs.length > 0) {
          var countEl = el('div', 'mf-list-count');
          countEl.textContent = msgs.length + ' message' + (msgs.length !== 1 ? 's' : '') + ' in list';
          msgContainer.appendChild(countEl);
        }

        col.appendChild(msgContainer);
        stackArea.appendChild(col);
      });
    }

    render();
  }

  /* ── Helper ───────────────────────────────────────── */
  function el(tag, className) {
    var e = document.createElement(tag);
    if (className) e.className = className;
    return e;
  }
})();

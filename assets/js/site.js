/**
 * NUGECID — Núcleo de Gestão do Conhecimento, Informação, Documentação e Memória
 * Polícia Científica do Rio Grande do Norte (PCIRN)
 * Interações Institucionais, Acessibilidade e Ferramentas
 */

(function () {
  'use strict';

  // ==========================================================================
  // 1. Barra de Acessibilidade Governamental (Padrão e-MAG)
  // ==========================================================================
  
  // Alto Contraste
  const contrastBtn = document.querySelector('[data-action="toggle-contrast"]');
  const savedContrast = localStorage.getItem('pci_high_contrast');
  
  if (savedContrast === 'true') {
    document.documentElement.classList.add('high-contrast');
    if (contrastBtn) contrastBtn.setAttribute('aria-pressed', 'true');
  }

  if (contrastBtn) {
    contrastBtn.addEventListener('click', () => {
      const isHigh = document.documentElement.classList.toggle('high-contrast');
      contrastBtn.setAttribute('aria-pressed', String(isHigh));
      localStorage.setItem('pci_high_contrast', String(isHigh));
    });
  }

  // Ajuste de Tamanho de Fonte
  const fontIncBtn = document.querySelector('[data-action="font-increase"]');
  const fontDecBtn = document.querySelector('[data-action="font-decrease"]');
  const fontResetBtn = document.querySelector('[data-action="font-reset"]');

  const FONT_LEVELS = [0.9, 1.0, 1.1, 1.2, 1.3];
  let currentFontIndex = 1; // default 1.0

  const savedFont = localStorage.getItem('pci_font_scale');
  if (savedFont) {
    const parsed = parseFloat(savedFont);
    const idx = FONT_LEVELS.indexOf(parsed);
    if (idx !== -1) {
      currentFontIndex = idx;
      applyFontScale(FONT_LEVELS[currentFontIndex]);
    }
  }

  function applyFontScale(scale) {
    document.documentElement.style.fontSize = `${scale * 100}%`;
    localStorage.setItem('pci_font_scale', String(scale));
  }

  if (fontIncBtn) {
    fontIncBtn.addEventListener('click', () => {
      if (currentFontIndex < FONT_LEVELS.length - 1) {
        currentFontIndex++;
        applyFontScale(FONT_LEVELS[currentFontIndex]);
      }
    });
  }

  if (fontDecBtn) {
    fontDecBtn.addEventListener('click', () => {
      if (currentFontIndex > 0) {
        currentFontIndex--;
        applyFontScale(FONT_LEVELS[currentFontIndex]);
      }
    });
  }

  if (fontResetBtn) {
    fontResetBtn.addEventListener('click', () => {
      currentFontIndex = 1;
      applyFontScale(1.0);
    });
  }

  // ==========================================================================
  // 2. Header Scroll & Mobile Navigation
  // ==========================================================================
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => {
      if (window.scrollY > 20) {
        header.classList.add('is-scrolled');
      } else {
        header.classList.remove('is-scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  const navToggle = document.querySelector('.nav-toggle');
  const siteNav = document.querySelector('.site-nav');
  if (navToggle && siteNav) {
    navToggle.addEventListener('click', () => {
      const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!isExpanded));
      siteNav.classList.toggle('is-open', !isExpanded);
      document.body.classList.toggle('nav-open', !isExpanded);
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && siteNav.classList.contains('is-open')) {
        navToggle.setAttribute('aria-expanded', 'false');
        siteNav.classList.remove('is-open');
        document.body.classList.remove('nav-open');
        navToggle.focus();
      }
    });
  }

  // ==========================================================================
  // 3. Scroll Reveal Animations (Intersection Observer)
  // ==========================================================================
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!prefersReducedMotion && 'IntersectionObserver' in window) {
    const revealElements = document.querySelectorAll('.reveal, .reveal-group > *');
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            obs.unobserve(entry.target);
          }
        });
      },
      {
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.1,
      }
    );

    revealElements.forEach((el) => observer.observe(el));
  } else {
    document.querySelectorAll('.reveal, .reveal-group > *').forEach((el) => {
      el.classList.add('is-visible');
    });
  }

  // ==========================================================================
  // 4. Visualizador Interativo de Telas (Lightbox Modal)
  // ==========================================================================
  const printFigures = document.querySelectorAll('.print img');
  if (printFigures.length > 0) {
    const modal = document.createElement('div');
    modal.className = 'screenshot-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Visualização de imagem do sistema');
    modal.innerHTML = `
      <div class="screenshot-modal-backdrop"></div>
      <div class="screenshot-modal-content">
        <button class="screenshot-modal-close" aria-label="Fechar visualização">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
        <img class="screenshot-modal-img" src="" alt="">
        <p class="screenshot-modal-caption"></p>
      </div>
    `;
    document.body.appendChild(modal);

    const modalImg = modal.querySelector('.screenshot-modal-img');
    const modalCaption = modal.querySelector('.screenshot-modal-caption');
    const closeBtn = modal.querySelector('.screenshot-modal-close');
    const backdrop = modal.querySelector('.screenshot-modal-backdrop');

    let lastFocusedElement = null;

    const openModal = (src, alt, caption) => {
      lastFocusedElement = document.activeElement;
      modalImg.src = src;
      modalImg.alt = alt;
      modalCaption.textContent = caption || alt;
      modal.classList.add('is-active');
      document.body.style.overflow = 'hidden';
      closeBtn.focus();
    };

    const closeModal = () => {
      modal.classList.remove('is-active');
      document.body.style.overflow = '';
      if (lastFocusedElement) {
        lastFocusedElement.focus();
      }
    };

    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('is-active')) {
        closeModal();
      }
    });

    printFigures.forEach((img) => {
      const figure = img.closest('figure');
      const caption = figure ? figure.querySelector('figcaption') : null;
      const captionText = caption ? caption.textContent.trim() : '';

      figure.classList.add('is-interactive-zoom');
      figure.setAttribute('tabindex', '0');
      figure.setAttribute('role', 'button');
      figure.setAttribute('aria-label', `Ampliar imagem: ${captionText || img.alt}`);

      const triggerOpen = () => openModal(img.src, img.alt, captionText);

      figure.addEventListener('click', triggerOpen);
      figure.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerOpen();
        }
      });
    });
  }

  // ==========================================================================
  // 5. Botões de Cópia (ISBN, ABNT, BibTeX)
  // ==========================================================================
  const copyButtons = document.querySelectorAll('[data-copy]');
  copyButtons.forEach((btn) => {
    btn.addEventListener('click', async () => {
      const textToCopy = btn.getAttribute('data-copy');
      if (!textToCopy) return;

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalText = btn.innerHTML;
        btn.classList.add('is-copied');
        btn.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          Copiado!
        `;
        setTimeout(() => {
          btn.classList.remove('is-copied');
          btn.innerHTML = originalText;
        }, 2200);
      } catch (err) {
        console.error('Falha ao copiar:', err);
      }
    });
  });

  // ==========================================================================
  // 6. Filtro Instantâneo em Notícias (noticias.html)
  // ==========================================================================
  const newsSearchInput = document.querySelector('#news-search');
  const newsCategoryBtns = document.querySelectorAll('[data-news-filter]');
  const newsCards = document.querySelectorAll('.news-card');
  const newsCountEl = document.querySelector('#news-count');
  const noNewsMsg = document.querySelector('#news-empty');

  if (newsCards.length > 0 && (newsSearchInput || newsCategoryBtns.length > 0)) {
    let activeCategory = 'all';
    let searchQuery = '';

    const filterNews = () => {
      let visibleCount = 0;

      newsCards.forEach((card) => {
        const text = card.textContent.toLowerCase();
        const category = card.getAttribute('data-category') || 'all';

        const matchesQuery = !searchQuery || text.includes(searchQuery);
        const matchesCategory = activeCategory === 'all' || category === activeCategory;

        if (matchesQuery && matchesCategory) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (newsCountEl) {
        newsCountEl.textContent = `${visibleCount} ${visibleCount === 1 ? 'notícia encontrada' : 'notícias encontradas'}`;
      }

      if (noNewsMsg) {
        noNewsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
      }
    };

    if (newsSearchInput) {
      newsSearchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        filterNews();
      });
    }

    newsCategoryBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        newsCategoryBtns.forEach((b) => b.classList.remove('is-active'));
        btn.classList.add('is-active');
        activeCategory = btn.getAttribute('data-news-filter') || 'all';
        filterNews();
      });
    });
  }

})();

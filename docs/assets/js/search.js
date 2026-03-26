(function() {
  let searchData = [];
  let fuse = null;
  let searchInput = null;
  let searchResults = null;
  let searchOverlay = null;
  let searchContainer = null;
  let siteHeader = null;
  let mobileSearchBtn = null;
  let searchCloseBtn = null;

  // Fuse.js options for Chinese-friendly fuzzy search
  const fuseOptions = {
    keys: [
      { name: 'title', weight: 0.4 },
      { name: 'content', weight: 0.4 },
      { name: 'excerpt', weight: 0.2 }
    ],
    threshold: 0.3,
    ignoreLocation: true,
    minMatchCharLength: 2,
    includeScore: true,
    includeMatches: true
  };

  // Initialize search
  async function initSearch() {
    searchInput = document.getElementById('search-input');
    searchResults = document.getElementById('search-results');
    searchOverlay = document.getElementById('search-overlay');
    searchContainer = document.getElementById('search-container');
    siteHeader = document.getElementById('site-header');
    mobileSearchBtn = document.getElementById('mobile-search-btn');
    searchCloseBtn = document.getElementById('search-close-btn');

    if (!searchInput || !searchResults) return;

    // Load search data
    try {
      const response = await fetch('/search.json');
      searchData = await response.json();
      fuse = new Fuse(searchData, fuseOptions);
    } catch (error) {
      console.error('Failed to load search data:', error);
      return;
    }

    // Bind events
    searchInput.addEventListener('input', debounce(handleSearch, 200));
    searchInput.addEventListener('focus', showResults);
    
    // Close results when clicking outside
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.search-container') && !e.target.closest('.mobile-search-btn')) {
        searchResults.innerHTML = '';
        hideResults();
      }
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', handleKeydown);

    // Global shortcut: press '/' to focus search
    document.addEventListener('keydown', function(e) {
      // Ignore if user is typing in an input/textarea
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      
      if (e.key === '/') {
        e.preventDefault();
        expandMobileSearch();
        searchInput.focus();
      }
    });

    // Mobile search expand/collapse
    if (mobileSearchBtn) {
      mobileSearchBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        expandMobileSearch();
      });
    }

    if (searchCloseBtn) {
      searchCloseBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        collapseMobileSearch();
      });
    }
  }

  function expandMobileSearch() {
    if (searchContainer && siteHeader) {
      searchContainer.classList.add('expanded');
      siteHeader.classList.add('search-expanded');
      setTimeout(() => searchInput.focus(), 100);
    }
  }

  function collapseMobileSearch() {
    if (searchContainer && siteHeader) {
      searchContainer.classList.remove('expanded');
      siteHeader.classList.remove('search-expanded');
      searchInput.value = '';
      searchResults.innerHTML = '';
      hideResults();
    }
  }

  function handleSearch() {
    const query = searchInput.value.trim();
    
    if (query.length < 2) {
      hideResults();
      return;
    }

    const results = fuse.search(query, { limit: 8 });
    displayResults(results, query);
  }

  function displayResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="search-no-results">No results found</div>';
      showResults();
      return;
    }

    const html = results.map((result, index) => {
      const item = result.item;
      const excerpt = highlightText(item.excerpt || '', query);
      
      return `
        <a href="${item.url}" class="search-result-item" data-index="${index}">
          <div class="search-result-title">${highlightText(item.title, query)}</div>
          <div class="search-result-excerpt">${excerpt}</div>
          <div class="search-result-date">${item.date}</div>
        </a>
      `;
    }).join('');

    searchResults.innerHTML = html;
    showResults();
  }

  function highlightText(text, query) {
    if (!query || !text) return text;
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function showResults() {
    if (searchResults.innerHTML) {
      searchResults.classList.add('show');
      if (searchOverlay) searchOverlay.classList.add('show');
    }
  }

  function hideResults() {
    searchResults.classList.remove('show');
    if (searchOverlay) searchOverlay.classList.remove('show');
  }

  function handleKeydown(e) {
    const items = searchResults.querySelectorAll('.search-result-item');
    const current = searchResults.querySelector('.search-result-item.active');
    let index = current ? parseInt(current.dataset.index) : -1;

    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        index = Math.min(index + 1, items.length - 1);
        break;
      case 'ArrowUp':
        e.preventDefault();
        index = Math.max(index - 1, 0);
        break;
      case 'Enter':
        if (current) {
          window.location.href = current.href;
        }
        return;
      case 'Escape':
        hideResults();
        collapseMobileSearch();
        searchInput.blur();
        return;
      default:
        return;
    }

    items.forEach(item => item.classList.remove('active'));
    if (items[index]) {
      items[index].classList.add('active');
    }
  }

  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearch);
  } else {
    initSearch();
  }
})();

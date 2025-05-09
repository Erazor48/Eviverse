// Fonction pour basculer entre les thèmes
function toggleTheme() {
    const darkThemeLink = document.getElementById('dark-theme-link');
    if (darkThemeLink) {
      // Si le thème sombre est actif, on le désactive
      darkThemeLink.remove();
      localStorage.setItem('theme', 'light');
      document.getElementById('theme-toggle').textContent = '🌙 Mode sombre';
    } else {
      // Si le thème sombre n'est pas actif, on l'active
      const link = document.createElement('link');
      link.id = 'dark-theme-link';
      link.rel = 'stylesheet';
      link.href = '/static/dark-theme.css';
      document.head.appendChild(link);
      localStorage.setItem('theme', 'dark');
      document.getElementById('theme-toggle').textContent = '☀️ Mode clair';
    }
  }
  
  // Fonction pour appliquer le thème sauvegardé et ajouter le bouton
  function applyTheme() {
    // Attendre que le DOM soit complètement chargé
    const theme = localStorage.getItem('theme') || 'light';
    
    // Créer le bouton
    const toggleButton = document.createElement('button');
    toggleButton.id = 'theme-toggle';
    toggleButton.style.position = 'fixed';
    toggleButton.style.top = '10px';
    toggleButton.style.right = '20px';
    toggleButton.style.zIndex = '9999'; // Valeur élevée pour s'assurer qu'il est au-dessus des autres éléments
    toggleButton.style.backgroundColor = '#444';
    toggleButton.style.color = 'white';
    toggleButton.style.border = 'none';
    toggleButton.style.borderRadius = '4px';
    toggleButton.style.padding = '8px 12px';
    toggleButton.style.cursor = 'pointer';
    toggleButton.style.fontSize = '14px';
    toggleButton.onclick = toggleTheme;
    
    // Définir le texte du bouton selon le thème actuel
    if (theme === 'dark') {
      const link = document.createElement('link');
      link.id = 'dark-theme-link';
      link.rel = 'stylesheet';
      link.href = '/static/dark-theme.css';
      document.head.appendChild(link);
      toggleButton.textContent = '☀️ Mode clair';
    } else {
      toggleButton.textContent = '🌙 Mode sombre';
    }
    
    // Ajouter le bouton au document
    document.body.appendChild(toggleButton);
  }
  
  // S'assurer que le DOM est complètement chargé avant d'ajouter le bouton
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTheme);
  } else {
    // Si le DOM est déjà chargé
    applyTheme();
  }
  
  // Pour Swagger UI, qui pourrait charger dynamiquement après le DOMContentLoaded
  // Ajouter une seconde tentative après un court délai
  setTimeout(function() {
    if (!document.getElementById('theme-toggle')) {
      applyTheme();
    }
  }, 1000);
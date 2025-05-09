// Script pour ajouter le toggle de mode sombre à ReDoc
document.addEventListener('DOMContentLoaded', function() {
    // On attend que ReDoc soit complètement chargé
    const checkReDocLoaded = setInterval(function() {
        // Vérifie si ReDoc est chargé en recherchant des éléments de sa structure
        if (document.querySelector('redoc') || 
            document.querySelector('[data-role="redoc"]') || 
            document.querySelector('[role="navigation"]')) {
            
            clearInterval(checkReDocLoaded);
            initDarkModeToggle();
        }
    }, 200);
    
    // Maximum de 5 secondes d'attente (25 tentatives à 200ms d'intervalle)
    setTimeout(() => {
        clearInterval(checkReDocLoaded);
        // Initialiser de toute façon après 5 secondes
        initDarkModeToggle();
    }, 5000);
});

function initDarkModeToggle() {
    // Création du bouton toggle avec animation
    const darkModeToggle = document.createElement('button');
    darkModeToggle.id = 'dark-mode-toggle';
    
    // Vérifier si le mode sombre est déjà activé (sauvegardé dans localStorage)
    const isDarkMode = localStorage.getItem('redoc-dark-mode') === 'true';
    
    // Définition du contenu du bouton avec icônes
    updateToggleButton(darkModeToggle, isDarkMode);
    
    // Appliquer le mode immédiatement au chargement
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
    
    // Ajout du bouton à la page
    document.body.appendChild(darkModeToggle);
    
    // Transition fluide pour les changements de thème
    const style = document.createElement('style');
    style.textContent = `
        body {
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        body * {
            transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        }
        #dark-mode-toggle {
            transition: background-color 0.2s ease, transform 0.1s ease;
        }
        #dark-mode-toggle:active {
            transform: scale(0.95);
        }
    `;
    document.head.appendChild(style);
    
    // Gestion du clic sur le bouton avec animation
    darkModeToggle.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('redoc-dark-mode', isDark);
        
        // Animation de transition
        darkModeToggle.style.transform = 'scale(0.9)';
        setTimeout(() => {
            darkModeToggle.style.transform = 'scale(1)';
            updateToggleButton(darkModeToggle, isDark);
        }, 100);
    });
    
    // Synchroniser l'état du thème avec d'autres onglets
    window.addEventListener('storage', function(event) {
        if (event.key === 'redoc-dark-mode') {
            const isDark = event.newValue === 'true';
            document.body.classList.toggle('dark-mode', isDark);
            updateToggleButton(darkModeToggle, isDark);
        }
    });
}

// Fonction pour mettre à jour l'apparence du bouton
function updateToggleButton(button, isDarkMode) {
    if (isDarkMode) {
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
            Mode clair
        `;
    } else {
        button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
            Mode sombre
        `;
    }
}
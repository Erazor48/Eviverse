// Script pour ajouter le toggle de mode sombre à Swagger UI
document.addEventListener('DOMContentLoaded', function() {
    // Création du bouton toggle
    const darkModeToggle = document.createElement('button');
    darkModeToggle.id = 'dark-mode-toggle';
    
    // Vérifier si le mode sombre est déjà activé (sauvegardé dans localStorage)
    const isDarkMode = localStorage.getItem('swagger-dark-mode') === 'true';
    
    // Définition du contenu du bouton avec icônes
    updateToggleButton(darkModeToggle, isDarkMode);
    
    // Appliquer le mode immédiatement au chargement
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
    }
    
    // Ajout du bouton à la page
    document.body.appendChild(darkModeToggle);
    
    // Gestion du clic sur le bouton
    darkModeToggle.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem('swagger-dark-mode', isDark);
        updateToggleButton(darkModeToggle, isDark);
    });
});

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
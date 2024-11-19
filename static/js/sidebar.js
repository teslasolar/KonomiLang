document.addEventListener('DOMContentLoaded', function() {
    // Load saved state
    const savedState = JSON.parse(localStorage.getItem('sidebarState') || '{}');
    
    // Get all accordion items
    const accordionItems = document.querySelectorAll('.accordion-item');
    
    // Initialize accordion items with saved state
    accordionItems.forEach(item => {
        const collapseElement = item.querySelector('.accordion-collapse');
        const buttonElement = item.querySelector('.accordion-button');
        const sectionId = collapseElement.id;
        
        // Apply saved state or default state
        if (savedState[sectionId] === true) {
            collapseElement.classList.add('show');
            buttonElement.classList.remove('collapsed');
        } else if (savedState[sectionId] === false) {
            collapseElement.classList.remove('show');
            buttonElement.classList.add('collapsed');
        }
        
        // Add click listener to save state
        buttonElement.addEventListener('click', () => {
            const isCollapsed = collapseElement.classList.contains('show');
            savedState[sectionId] = !isCollapsed;
            localStorage.setItem('sidebarState', JSON.stringify(savedState));
        });
    });
});

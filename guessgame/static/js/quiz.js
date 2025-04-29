document.addEventListener('DOMContentLoaded', () => {
    const lifelineButtons = document.querySelectorAll('.lifelines button');
    
    lifelineButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.clue-card');
            const clueId = card.dataset.clueId;
            
            if(e.target.classList.contains('hint-btn')) {
                fetch(`/quiz/hint/${clueId}/`)
                    .then(response => response.json())
                    .then(data => showHint(data.hint));
            }
        });
    });
});

function showHint(hintContent) {
    // Implement hint display logic
}
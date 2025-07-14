// Fix simple para Enter - agregar al final de voice-chat.js
// o ejecutar en la consola del navegador

(function() {
    const input = document.getElementById('textInput');
    if (input) {
        // Remover eventos anteriores
        const newInput = input.cloneNode(true);
        input.parentNode.replaceChild(newInput, input);
        
        // Agregar nuevo evento
        newInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const sendBtn = document.getElementById('sendBtn');
                if (sendBtn) {
                    sendBtn.click();
                }
            }
        });
        console.log('Enter key fix aplicado');
    }
})();


/**
 * Custom Rich Text Editor Implementation
 * 
 * This is a lightweight custom rich text editor for specific use cases.
 * For email composition and advanced editing, the system uses CKEditor 5 (loaded via CDN).
 * This custom editor provides basic formatting for description fields throughout the application.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize custom rich text editors for elements with .rich-editor class
    const richEditors = document.querySelectorAll('.rich-editor');
    
    richEditors.forEach(function(editor) {
        // Create toolbar
        const toolbar = document.createElement('div');
        toolbar.className = 'rich-toolbar';
        toolbar.style.cssText = `
            background: #374151;
            border: 1px solid #4b5563;
            border-bottom: none;
            padding: 8px;
            border-radius: 4px 4px 0 0;
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        `;

        // Define toolbar buttons
        const buttons = [
            {text: 'B', cmd: 'bold', title: 'Bold'},
            {text: 'I', cmd: 'italic', title: 'Italic'},
            {text: 'U', cmd: 'underline', title: 'Underline'},
            {text: 'H1', cmd: 'formatBlock', value: '<h1>', title: 'Heading 1'},
            {text: 'H2', cmd: 'formatBlock', value: '<h2>', title: 'Heading 2'},
            {text: 'H3', cmd: 'formatBlock', value: '<h3>', title: 'Heading 3'},
            {text: 'P', cmd: 'formatBlock', value: '<p>', title: 'Paragraph'},
            {text: '•', cmd: 'insertUnorderedList', title: 'Bullet List'},
            {text: '1.', cmd: 'insertOrderedList', title: 'Numbered List'},
            {text: '"', cmd: 'formatBlock', value: '<blockquote>', title: 'Quote'},
        ];

        // Create buttons
        buttons.forEach(function(btn) {
            const button = document.createElement('button');
            button.type = 'button';
            button.innerHTML = btn.text;
            button.title = btn.title;
            button.style.cssText = `
                background: #4b5563;
                color: white;
                border: 1px solid #6b7280;
                padding: 4px 8px;
                border-radius: 3px;
                cursor: pointer;
                font-size: 12px;
                font-weight: bold;
            `;
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                contentDiv.focus();
                if (btn.value) {
                    document.execCommand(btn.cmd, false, btn.value);
                } else {
                    document.execCommand(btn.cmd, false, null);
                }
                updateTextarea();
            });
            
            button.addEventListener('mouseover', function() {
                this.style.background = '#6b7280';
            });
            
            button.addEventListener('mouseout', function() {
                this.style.background = '#4b5563';
            });
            
            toolbar.appendChild(button);
        });

        // Create content editable div
        const contentDiv = document.createElement('div');
        contentDiv.contentEditable = true;
        contentDiv.style.cssText = `
            min-height: 200px;
            padding: 15px;
            border: 1px solid #4b5563;
            border-top: none;
            border-radius: 0 0 4px 4px;
            background: white;
            color: #1f2937;
            line-height: 1.6;
            font-family: Georgia, serif;
            outline: none;
        `;
        contentDiv.innerHTML = editor.value || '<p>Start writing your detailed description...</p>';

        // Hide original textarea
        editor.style.display = 'none';

        // Insert toolbar and content div before textarea
        editor.parentNode.insertBefore(toolbar, editor);
        editor.parentNode.insertBefore(contentDiv, editor);

        // Update textarea when content changes
        function updateTextarea() {
            editor.value = contentDiv.innerHTML;
        }

        // Update content div when textarea changes (for form validation)
        editor.addEventListener('input', function() {
            if (editor.value !== contentDiv.innerHTML) {
                contentDiv.innerHTML = editor.value;
            }
        });

        // Update textarea on content change
        contentDiv.addEventListener('input', updateTextarea);
        contentDiv.addEventListener('paste', function(e) {
            // Clean pasted content
            setTimeout(updateTextarea, 10);
        });

        // Focus management
        contentDiv.addEventListener('focus', function() {
            this.style.borderColor = '#3b82f6';
        });
        
        contentDiv.addEventListener('blur', function() {
            this.style.borderColor = '#4b5563';
            updateTextarea();
        });
    });
});

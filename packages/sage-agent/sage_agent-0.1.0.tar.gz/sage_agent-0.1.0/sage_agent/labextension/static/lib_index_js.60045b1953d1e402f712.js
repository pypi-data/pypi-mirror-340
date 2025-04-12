"use strict";
(self["webpackChunksage_agent"] = self["webpackChunksage_agent"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);




/**
 * ChatBoxWidget: A widget for interacting with OpenAI via a chat interface
 */
class ChatBoxWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this.apiKey = '';
        this.inferenceUrl = 'https://api.alpinex.ai/v1/chat/completions';
        this.modelName = 'Meta-Llama-3.1-405B-Instruct-Turbo';
        this.messageHistory = [];
        this.id = 'sage-agent-chat';
        this.title.label = 'AI Chat';
        this.title.closable = true;
        this.addClass('sage-agent-chatbox');
        // Create layout for the chat box
        const layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout();
        this.layout = layout;
        // Create chat history container
        const historyContainer = document.createElement('div');
        historyContainer.className = 'sage-agent-history-container';
        this.chatHistory = document.createElement('div');
        this.chatHistory.className = 'sage-agent-chat-history';
        historyContainer.appendChild(this.chatHistory);
        // Create input container with text input and send button
        const inputContainer = document.createElement('div');
        inputContainer.className = 'sage-agent-input-container';
        this.chatInput = document.createElement('input');
        this.chatInput.className = 'sage-agent-chat-input';
        this.chatInput.placeholder = 'Ask your question...';
        this.chatInput.addEventListener('keydown', event => {
            if (event.key === 'Enter' && this.chatInput.value.trim() !== '') {
                this.sendMessage();
            }
        });
        this.sendButton = document.createElement('button');
        this.sendButton.className = 'sage-agent-send-button';
        this.sendButton.textContent = 'Send';
        this.sendButton.addEventListener('click', () => {
            if (this.chatInput.value.trim() !== '') {
                this.sendMessage();
            }
        });
        inputContainer.appendChild(this.chatInput);
        inputContainer.appendChild(this.sendButton);
        // Add history and input containers to the layout
        layout.addWidget(new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget({ node: historyContainer }));
        layout.addWidget(new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget({ node: inputContainer }));
        // Add welcome message
        this.addSystemMessage(`Welcome to AI Chat! Using model: ${this.modelName}`);
    }
    /**
     * Handle a message after the widget is shown.
     */
    onAfterShow(msg) {
        this.chatInput.focus();
    }
    /**
     * Set the OpenAI API key
     */
    setApiKey(apiKey) {
        this.apiKey = apiKey;
        if (!apiKey) {
            this.addSystemMessage('⚠️ No API key set. Please configure it in the settings.');
        }
        else {
            this.addSystemMessage('API key configured successfully.');
        }
    }
    /**
     * Set the inference URL
     */
    setInferenceUrl(url) {
        this.inferenceUrl = url || 'https://api.alpinex.ai/v1/chat/completions';
        this.addSystemMessage(`Inference URL set to: ${this.inferenceUrl}`);
    }
    /**
     * Set the model name
     */
    setModelName(model) {
        if (model && model !== this.modelName) {
            this.modelName = model;
            this.addSystemMessage(`Model changed to: ${this.modelName}`);
        }
    }
    /**
     * Add a user message to the chat history
     */
    addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'sage-agent-message sage-agent-user-message';
        messageElement.innerHTML = `<strong>You:</strong> ${message}`;
        this.chatHistory.appendChild(messageElement);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
        // Add to message history for context
        this.messageHistory.push({ role: 'user', content: message });
    }
    /**
     * Add an AI response to the chat history
     */
    addAIResponse(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'sage-agent-message sage-agent-ai-message';
        messageElement.innerHTML = `<strong>AI:</strong> ${message}`;
        this.chatHistory.appendChild(messageElement);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
        // Add to message history for context
        this.messageHistory.push({ role: 'assistant', content: message });
    }
    /**
     * Add a system message to the chat history
     */
    addSystemMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'sage-agent-message sage-agent-system-message';
        messageElement.textContent = message;
        this.chatHistory.appendChild(messageElement);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
    }
    /**
     * Send a message to the OpenAI API
     */
    async sendMessage() {
        var _a;
        const message = this.chatInput.value.trim();
        if (!message) {
            return;
        }
        this.addUserMessage(message);
        this.chatInput.value = '';
        if (!this.apiKey) {
            this.addSystemMessage('❌ API key is not set. Please configure it in the settings.');
            return;
        }
        // Add a loading indicator
        const loadingElement = document.createElement('div');
        loadingElement.className = 'sage-agent-message sage-agent-loading';
        loadingElement.textContent = 'AI is thinking...';
        this.chatHistory.appendChild(loadingElement);
        this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
        try {
            // Prepare the messages for the API, including context
            const messages = [...this.messageHistory];
            // Make API call
            const response = await fetch(this.inferenceUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${this.apiKey}`
                },
                body: JSON.stringify({
                    model: this.modelName,
                    messages: messages.slice(-10) // Only send last 10 messages to avoid token limits
                })
            });
            // Remove loading indicator
            this.chatHistory.removeChild(loadingElement);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(((_a = errorData.error) === null || _a === void 0 ? void 0 : _a.message) || `Error: ${response.statusText}`);
            }
            const data = await response.json();
            const reply = data.choices[0].message.content;
            this.addAIResponse(reply);
        }
        catch (error) {
            // Remove loading indicator
            if (loadingElement.parentNode === this.chatHistory) {
                this.chatHistory.removeChild(loadingElement);
            }
            // Show error message
            this.addSystemMessage(`❌ ${error instanceof Error ? error.message : 'An error occurred while communicating with the AI service.'}`);
        }
    }
}
/**
 * Initialization data for the sage-agent extension.
 */
const plugin = {
    id: 'sage-agent:plugin',
    description: 'Sage AI - Your AI Data Partner',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    activate: (app, palette, settingRegistry) => {
        console.log('JupyterLab extension sage-agent is activated!');
        // Create a widget tracker to keep track of the chat widgets
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'sage-agent-chat'
        });
        // Create a new chat widget
        const createChatWidget = () => {
            const chatWidget = new ChatBoxWidget();
            tracker.add(chatWidget);
            // Add the chat widget to the right side panel
            app.shell.add(chatWidget, 'right', { rank: 1000 });
            return chatWidget;
        };
        // Create the initial chat widget
        let chatWidget = createChatWidget();
        // Function to load settings
        const loadSettings = (settings) => {
            // Get the API key from the settings
            const apiKey = settings.get('apiKey').composite;
            chatWidget.setApiKey(apiKey);
            // Get the inference URL from the settings
            const inferenceUrl = settings.get('inferenceUrl').composite;
            chatWidget.setInferenceUrl(inferenceUrl);
            // Get the model name from the settings
            const modelName = settings.get('modelName').composite;
            chatWidget.setModelName(modelName);
            // Listen for setting changes
            settings.changed.connect(() => {
                const updatedApiKey = settings.get('apiKey').composite;
                const updatedInferenceUrl = settings.get('inferenceUrl')
                    .composite;
                const updatedModelName = settings.get('modelName').composite;
                chatWidget.setApiKey(updatedApiKey);
                chatWidget.setInferenceUrl(updatedInferenceUrl);
                chatWidget.setModelName(updatedModelName);
            });
        };
        // Load settings if available
        if (settingRegistry) {
            Promise.all([settingRegistry.load(plugin.id), app.restored])
                .then(([settings]) => {
                loadSettings(settings);
            })
                .catch(error => {
                console.error('Failed to load sage-agent settings', error);
            });
        }
        // Add an application command to open the chat widget
        const command = 'sage-agent:open-chat';
        app.commands.addCommand(command, {
            label: 'Open AI Chat',
            execute: () => {
                // If the widget is disposed, create a new one
                if (chatWidget.isDisposed) {
                    chatWidget = createChatWidget();
                }
                // If the widget is not attached to the DOM, add it
                if (!chatWidget.isAttached) {
                    app.shell.add(chatWidget, 'right', { rank: 1000 });
                }
                // Activate the widget
                app.shell.activateById(chatWidget.id);
            }
        });
        // Add the command to the command palette
        palette.addItem({ command, category: 'AI Tools' });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.60045b1953d1e402f712.js.map
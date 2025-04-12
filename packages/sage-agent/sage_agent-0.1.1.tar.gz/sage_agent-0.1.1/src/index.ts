import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ICommandPalette, WidgetTracker } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { PanelLayout } from '@lumino/widgets';
import { Message } from '@lumino/messaging';

/**
 * ChatBoxWidget: A widget for interacting with OpenAI via a chat interface
 */
class ChatBoxWidget extends Widget {
  private chatHistory: HTMLDivElement;
  private chatInput: HTMLInputElement;
  private sendButton: HTMLButtonElement;
  private apiKey: string = '';
  private inferenceUrl: string = 'https://api.alpinex.ai/v1/chat/completions';
  private modelName: string = 'Meta-Llama-3.1-405B-Instruct-Turbo';
  private messageHistory: Array<{ role: string; content: string }> = [];

  constructor() {
    super();
    this.id = 'sage-ai-chat';
    this.title.label = 'AI Chat';
    this.title.closable = true;
    this.addClass('sage-ai-chatbox');

    // Create layout for the chat box
    const layout = new PanelLayout();
    this.layout = layout;

    // Create chat history container
    const historyContainer = document.createElement('div');
    historyContainer.className = 'sage-ai-history-container';
    this.chatHistory = document.createElement('div');
    this.chatHistory.className = 'sage-ai-chat-history';
    historyContainer.appendChild(this.chatHistory);

    // Create input container with text input and send button
    const inputContainer = document.createElement('div');
    inputContainer.className = 'sage-ai-input-container';

    this.chatInput = document.createElement('input');
    this.chatInput.className = 'sage-ai-chat-input';
    this.chatInput.placeholder = 'Ask your question...';
    this.chatInput.addEventListener('keydown', event => {
      if (event.key === 'Enter' && this.chatInput.value.trim() !== '') {
        this.sendMessage();
      }
    });

    this.sendButton = document.createElement('button');
    this.sendButton.className = 'sage-ai-send-button';
    this.sendButton.textContent = 'Send';
    this.sendButton.addEventListener('click', () => {
      if (this.chatInput.value.trim() !== '') {
        this.sendMessage();
      }
    });

    inputContainer.appendChild(this.chatInput);
    inputContainer.appendChild(this.sendButton);

    // Add history and input containers to the layout
    layout.addWidget(new Widget({ node: historyContainer }));
    layout.addWidget(new Widget({ node: inputContainer }));

    // Add welcome message
    this.addSystemMessage(`Welcome to AI Chat! Using model: ${this.modelName}`);
  }

  /**
   * Handle a message after the widget is shown.
   */
  protected onAfterShow(msg: Message): void {
    this.chatInput.focus();
  }

  /**
   * Set the OpenAI API key
   */
  setApiKey(apiKey: string): void {
    this.apiKey = apiKey;
    if (!apiKey) {
      this.addSystemMessage(
        '⚠️ No API key set. Please configure it in the settings.'
      );
    } else {
      this.addSystemMessage('API key configured successfully.');
    }
  }

  /**
   * Set the inference URL
   */
  setInferenceUrl(url: string): void {
    this.inferenceUrl = url || 'https://api.alpinex.ai/v1/chat/completions';
    this.addSystemMessage(`Inference URL set to: ${this.inferenceUrl}`);
  }

  /**
   * Set the model name
   */
  setModelName(model: string): void {
    if (model && model !== this.modelName) {
      this.modelName = model;
      this.addSystemMessage(`Model changed to: ${this.modelName}`);
    }
  }

  /**
   * Add a user message to the chat history
   */
  private addUserMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-user-message';
    messageElement.innerHTML = `<strong>You:</strong> ${message}`;
    this.chatHistory.appendChild(messageElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;

    // Add to message history for context
    this.messageHistory.push({ role: 'user', content: message });
  }

  /**
   * Add an AI response to the chat history
   */
  private addAIResponse(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-ai-message';
    messageElement.innerHTML = `<strong>AI:</strong> ${message}`;
    this.chatHistory.appendChild(messageElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;

    // Add to message history for context
    this.messageHistory.push({ role: 'assistant', content: message });
  }

  /**
   * Add a system message to the chat history
   */
  private addSystemMessage(message: string): void {
    const messageElement = document.createElement('div');
    messageElement.className = 'sage-ai-message sage-ai-system-message';
    messageElement.textContent = message;
    this.chatHistory.appendChild(messageElement);
    this.chatHistory.scrollTop = this.chatHistory.scrollHeight;
  }

  /**
   * Send a message to the OpenAI API
   */
  private async sendMessage(): Promise<void> {
    const message = this.chatInput.value.trim();
    if (!message) {
      return;
    }

    this.addUserMessage(message);
    this.chatInput.value = '';

    if (!this.apiKey) {
      this.addSystemMessage(
        '❌ API key is not set. Please configure it in the settings.'
      );
      return;
    }

    // Add a loading indicator
    const loadingElement = document.createElement('div');
    loadingElement.className = 'sage-ai-message sage-ai-loading';
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
        throw new Error(
          errorData.error?.message || `Error: ${response.statusText}`
        );
      }

      const data = await response.json();
      const reply = data.choices[0].message.content;
      this.addAIResponse(reply);
    } catch (error) {
      // Remove loading indicator
      if (loadingElement.parentNode === this.chatHistory) {
        this.chatHistory.removeChild(loadingElement);
      }

      // Show error message
      this.addSystemMessage(
        `❌ ${error instanceof Error ? error.message : 'An error occurred while communicating with the AI service.'}`
      );
    }
  }
}

/**
 * Initialization data for the sage-ai extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'sage-agent:plugin',
  description: 'Sage AI - Your AI Data Partner',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.log('JupyterLab extension sage-agent is activated!');

    // Create a widget tracker to keep track of the chat widgets
    const tracker = new WidgetTracker<ChatBoxWidget>({
      namespace: 'sage-ai-chat'
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
    const loadSettings = (settings: ISettingRegistry.ISettings) => {
      // Get the API key from the settings
      const apiKey = settings.get('apiKey').composite as string;
      chatWidget.setApiKey(apiKey);

      // Get the inference URL from the settings
      const inferenceUrl = settings.get('inferenceUrl').composite as string;
      chatWidget.setInferenceUrl(inferenceUrl);

      // Get the model name from the settings
      const modelName = settings.get('modelName').composite as string;
      chatWidget.setModelName(modelName);

      // Listen for setting changes
      settings.changed.connect(() => {
        const updatedApiKey = settings.get('apiKey').composite as string;
        const updatedInferenceUrl = settings.get('inferenceUrl')
          .composite as string;
        const updatedModelName = settings.get('modelName').composite as string;

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
          console.error('Failed to load sage-ai settings', error);
        });
    }

    // Add an application command to open the chat widget
    const command: string = 'sage-ai:open-chat';
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

export default plugin;

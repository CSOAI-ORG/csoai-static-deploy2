// SOV-Space Chrome Extension — Background Service Worker
// Connects to local Ollama and SOV-space API

const OLLAMA_URL = 'http://localhost:11434';
const SOV_API = 'http://localhost:3001';

// Call Ollama model
async function callOllama(model, prompt) {
  try {
    const response = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        model: model,
        prompt: prompt,
        stream: false,
        options: {temperature: 0, num_predict: 256}
      })
    });
    const data = await response.json();
    return {ok: true, response: data.response?.trim() || ''};
  } catch (e) {
    return {ok: false, error: e.message};
  }
}

// Ask SOV-space
async function askSOV(question) {
  // Try models in order of capability
  const models = ['sov-sovereign-v2', 'sov-general', 'sov-reasoning'];
  
  for (const model of models) {
    const result = await callOllama(model, `Answer briefly: ${question}`);
    if (result.ok && result.response) {
      return {
        answer: result.response,
        model: model,
        timestamp: new Date().toISOString()
      };
    }
  }
  
  return {answer: 'No model available. Is Ollama running?', model: 'none'};
}

// Get SOV-space status
async function getStatus() {
  try {
    const response = await fetch(`${SOV_API}/api/status`);
    return await response.json();
  } catch (e) {
    return {error: e.message};
  }
}

// Listen for messages from popup/content
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === 'ask') {
    askSOV(msg.question).then(result => {
      sendResponse(result);
    });
    return true; // Keep message channel open for async response
  }
  
  if (msg.action === 'status') {
    getStatus().then(result => {
      sendResponse(result);
    });
    return true;
  }
  
  if (msg.action === 'model') {
    callOllama(msg.model, msg.prompt).then(result => {
      sendResponse(result);
    });
    return true;
  }
});

// Context menu integration
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'askSOV',
    title: 'Ask SOV-Space: "%s"',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'askSOV' && info.selectionText) {
    askSOV(info.selectionText).then(result => {
      chrome.tabs.sendMessage(tab.id, {
        action: 'showAnswer',
        answer: result.answer,
        model: result.model
      });
    });
  }
});

console.log('SOV-Space Chrome Extension loaded');

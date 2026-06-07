const apiButtons = document.querySelectorAll('#apiButton, #apiButtonAlt');
const apiResult = document.getElementById('apiResult');
const dreamForm = document.getElementById('dreamForm');
const dreamsContainer = document.getElementById('dreams');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const authNotice = document.getElementById('authNotice');
const settingsStatus = document.getElementById('settingsStatus');
const accountDetails = document.getElementById('accountDetails');
const userName = document.getElementById('userName');
const userEmail = document.getElementById('userEmail');
const userId = document.getElementById('userId');
const darkModeToggle = document.getElementById('darkModeToggle');
const oauthStatus = document.getElementById('oauthStatus');
const baseUrlDisplay = document.getElementById('baseUrlDisplay');
const storageMode = document.getElementById('storageMode');

const DARK_MODE_KEY = 'trip-dreams-dark-mode';

function renderDreams(dreams) {
  if (!dreams || dreams.length === 0) {
    dreamsContainer.innerHTML = '<p class="empty-state">No dreams added yet. Add your first destination to see it here.</p>';
    return;
  }

  dreamsContainer.innerHTML = dreams
    .map(
      (dream) => `
      <article class="dream-card">
        <div>
          <strong>${dream.location}</strong>
          <div>${dream.priority} priority · $${dream.budget}</div>
        </div>
        <div>${new Date(dream.createdAt * 1000).toLocaleDateString()}</div>
      </article>
    `
    )
    .join('');
}

function applyDarkMode(enabled) {
  document.body.classList.toggle('theme-dark', enabled);
  localStorage.setItem(DARK_MODE_KEY, enabled ? 'true' : 'false');
}

async function loadAppConfig() {
  try {
    const response = await fetch('/api/config');
    const config = await response.json();
    oauthStatus.textContent = config.oauth_enabled ? 'Enabled' : 'Disabled';
    baseUrlDisplay.textContent = config.base_url || 'Not set';
    storageMode.textContent = config.firestore_available ? 'Firestore' : 'Local browser storage';
  } catch (error) {
    oauthStatus.textContent = 'Unavailable';
    baseUrlDisplay.textContent = 'Unavailable';
    storageMode.textContent = 'Unavailable';
  }
}

async function handleApiCall() {
  apiResult.textContent = 'Loading...';
  try {
    const response = await fetch('/api/hello');
    const data = await response.json();
    apiResult.textContent = data.message;
  } catch (error) {
    apiResult.textContent = 'Failed to reach the API. Open the terminal and run the server.';
  }
}

async function fetchDreams() {
  try {
    const response = await fetch('/api/dreams');
    if (!response.ok) {
      throw new Error('API unavailable');
    }
    const dreams = await response.json();
    renderDreams(dreams);
  } catch (error) {
    dreamsContainer.innerHTML = '<p class="empty-state">Unable to load dreams. Make sure the backend is running.</p>';
  }
}

async function checkAuth() {
  try {
    const [configRes, authRes] = await Promise.all([fetch('/api/config'), fetch('/api/me')]);
    const config = await configRes.json();
    const auth = await authRes.json();

    if (!config.oauth_enabled) {
      loginBtn.style.display = 'none';
      logoutBtn.style.display = 'none';
      authNotice.textContent = 'Google OAuth is currently disabled. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your environment to enable login.';
      return;
    }

    if (auth.logged_in) {
      loginBtn.style.display = 'none';
      logoutBtn.style.display = 'inline-block';
      settingsStatus.textContent = 'You are signed in with Google.';
      accountDetails.style.display = 'block';
      userName.textContent = auth.user?.name ? `Name: ${auth.user.name}` : '';
      userEmail.textContent = auth.user?.email ? `Email: ${auth.user.email}` : '';
      userId.textContent = auth.user?.sub ? `Google ID: ${auth.user.sub}` : '';
      authNotice.textContent = `Signed in as ${auth.user?.email || 'your Google account'}. Use Log out to disconnect.`;
    } else {
      loginBtn.style.display = 'inline-block';
      logoutBtn.style.display = 'none';
      settingsStatus.textContent = 'You are not signed in.';
      accountDetails.style.display = 'none';
      authNotice.textContent = 'Log in to save dreams and access your account settings.';
    }
  } catch (e) {
    // ignore
  }
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const location = document.getElementById('location').value.trim();
  const priority = document.getElementById('priority').value;
  const budget = Number(document.getElementById('budget').value);

  if (!location || !budget) {
    return;
  }

  try {
    const response = await fetch('/api/dreams', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ location, priority, budget }),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(text || 'Failed to save dream');
    }

    dreamForm.reset();
    fetchDreams();
  } catch (error) {
    apiResult.textContent = 'Unable to save dream. You may need to log in first.';
  }
}

apiButtons.forEach((button) => {
  button.addEventListener('click', handleApiCall);
});

darkModeToggle?.addEventListener('change', (event) => {
  applyDarkMode(event.target.checked);
});

function loadSettings() {
  const darkMode = localStorage.getItem(DARK_MODE_KEY) === 'true';
  darkModeToggle.checked = darkMode;
  applyDarkMode(darkMode);
}

dreamForm.addEventListener('submit', handleFormSubmit);
loadSettings();
fetchDreams();
loadAppConfig();
checkAuth();

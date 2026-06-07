const apiButtons = document.querySelectorAll('#apiButton, #apiButtonAlt');
const apiResult = document.getElementById('apiResult');
const dreamForm = document.getElementById('dreamForm');
const dreamsContainer = document.getElementById('dreams');

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
      throw new Error('Failed to save dream');
    }

    dreamForm.reset();
    fetchDreams();
  } catch (error) {
    apiResult.textContent = 'Unable to save dream. Check backend or Firestore configuration.';
  }
}

apiButtons.forEach((button) => {
  button.addEventListener('click', handleApiCall);
});

dreamForm.addEventListener('submit', handleFormSubmit);
fetchDreams();

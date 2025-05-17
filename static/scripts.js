function loadVideo() {
    const url = document.getElementById('url').value;

    fetch('/subtitles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => displaySubtitles(data));

    document.getElementById('player').innerHTML = 
        `<iframe width="560" height="315" src="https://www.youtube.com/embed/${getVideoId(url)}" frameborder="0" allowfullscreen></iframe>`;
}

function getVideoId(url) {
    return url.split('v=')[1].split('&')[0];
}

function displaySubtitles(subs) {
    const container = document.getElementById('subtitles');
    container.innerHTML = '';

    subs.forEach(item => {
        const sentence = item.text;
        const words = sentence.split(/\s+/);

        const sentenceDiv = document.createElement('div');

        words.forEach(word => {
            const span = document.createElement('span');
            span.innerText = word + ' ';
            span.style.cursor = 'pointer';
            span.style.color = 'blue';
            span.onclick = () => sendToChatbot(word.replace(/[^\w']/g, ''), sentence); // Strip punctuation from word only
            sentenceDiv.appendChild(span);
        });

        container.appendChild(sentenceDiv);
    });
}


function sendToChatbot(word, sentence) {
    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: word, sentence: sentence })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('chatbot-response').innerText = data.response;
    });
}
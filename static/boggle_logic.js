//Form
const guessWordForm = $('#guess');
const guessWordField = $('#word');

//Sidebar
const guessHistory = $('#list');
const scoreUI = $('#score');
const highscoreUI = $('#highscore');
const timerUI = $('#timer');

let gameComplete = false;
let score = 0;
start = Date.now();

const timerInterval = setInterval(function() {
    let time = 60 - Math.floor((new Date - start) / 1000)
    if(time > 0)
        timerUI.text(`Timer: ${time}`);
    else {
        handleGameEnd();
        clearInterval(timerInterval);
    }
}, 1000);

guessWordForm.on('submit', (e) => {
    e.preventDefault();
    if(gameComplete) return
    guessWord(guessWordField.val());
    guessWordField.val("");
});

async function guessWord(word){
    const result = await axios.get(`/guess/${word}`);
    if(result.data == "ok") {
        score += word.length;
        scoreUI.text(score);
    }
    guessHistory.append(createHistoryHTML(result.data, word));
}

function createHistoryHTML(result, word){
    if(result == "ok")
        return `<li class="text-success"><span>${word}</span> was found, +${word.length} points!</li>`;
    else if(result == "not-word")
        return `<li class="text-danger"><span>${word}</span> is not in our dictionary.</li>`;
    else if(result == "not-on-board")
        return `<li class="text-warning"><span>${word}</span> is not on board.</li>`;
    else if(result == "repeat")
        return `<li class="text-warning"><span>${word}</span> has already been counted.</li>`;
    return `<li class="text-warning">Something went terribly wrong</li>`;
}

function handleGameEnd(){
    timerUI.text("Game Complete");
    timerUI.addClass("text-primary");
    gameComplete = true;
    guessWordField.attr("disabled", "disabled");
    completeGame(score);
    if(score>highscoreUI.val()){
        highscoreUI.text(score);
    }
    guessWordForm.after("<a href='/' class='btn btn-outline-success mt-3'>New Game?</a>")
}

async function completeGame(newScore){
    await axios.post('/complete',  { scored: newScore });
}
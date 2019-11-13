// require https://unpkg.com/react@16/umd/react.development.js
// require https://unpkg.com/react-dom@16/umd/react-dom.development.js
// require Ur.css

function SquareRed(props) {
  return (
    <button className="square square-red" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

function Square(props) {
  return (
    <button className="square square-white" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

function Square_nb(props) {
return (
  <button className="square square-nb" onClick={props.onClick}>
    {props.value}
  </button>
);
}

class Board extends React.Component {
renderSquareRed(i) {
  return (
    <SquareRed
      value={this.props.squares[i]}
      onClick={() => this.props.onClick(i)}
    />
  );
}

renderSquare(i) {
  return (
    <Square
      value={this.props.squares[i]}
      onClick={() => this.props.onClick(i)}
    />
  );
}

renderSquare_nb(i) {
    return (
      <Square_nb
        value={this.props.squares[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
}

renderSquare_nb_noClick(i) {
  return (
    <Square_nb
      value={this.props.squares[i]}
    />
  );
}

render() {
  return (
    <div>
      <div className="board-row">
        {this.renderSquareRed(0)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(3)}
        {this.renderSquare_nb(4)}
        {this.renderSquare_nb(5)}
        {this.renderSquareRed(6)}
        {this.renderSquare(7)}
      </div>
      <div className="board-row">
        {this.renderSquare(8)}
        {this.renderSquare(9)}
        {this.renderSquare(10)}
        {this.renderSquareRed(11)}
        {this.renderSquare(12)}
        {this.renderSquare(13)}
        {this.renderSquare(14)}
        {this.renderSquare(15)}
      </div>
      <div className="board-row">
        {this.renderSquareRed(16)}
        {this.renderSquare(17)}
        {this.renderSquare(18)}
        {this.renderSquare(19)}
        {this.renderSquare_nb(20)}
        {this.renderSquare_nb(21)}
        {this.renderSquareRed(22)}
        {this.renderSquare(23)}
      </div>
    </div>
  );
}
}

class Game extends React.Component {

constructor(props) {
  let keyLength = 6;
  let r = generateId().substring(0,keyLength);
  console.log("Game Key: ", r);
  super(props);
  this.state = {
    gameKey: r.toUpperCase(),
    currentDisplay: Array(40).fill(""),
    diceRoll: -1
  };

  this.handleGameKeyChange = this.handleGameKeyChange.bind(this);
  this.handleGameKeySubmit = this.handleGameKeySubmit.bind(this);
}

componentDidMount() {
  this.intervalID = setInterval(
    () => sendDataToServer(this, {
      clickPosition: -1,
      game_key: this.state.gameKey
    }),
    1000
  );
}

componentWillUnmount() {
  clearInterval(this.intervalID);
}

handleClick(i) {
  //const newState = this.state.currentDisplay.slice();
  //newState[i] = this.state.xIsNext ? "X" : "O";
  //this.state.xIsNext = !this.state.xIsNext;
  //this.setState({
  //  currentDisplay : newState
  //});
  // this.getData(i);
  var data = {
    clickPosition: i,
    game_key: this.state.gameKey,
  };

  sendDataToServer(this, data);
}

// getData(i) {
//   // create a new XMLHttpRequest
//   var xhr = new XMLHttpRequest()
//   xhr.responseType = 'json';
//   // get a callback when the server responds
//   xhr.open('POST', 'http://localhost:2081/hiddenRequest')
//   xhr.onload  = function() {
//     var testVal = xhr.response['gameState'];
//   }
//   xhr.send(JSON.stringify({ 'clickPosition': i }))
// }

handleGameKeySubmit(event) {
  this.state.gameKey = this.state.gameKey.toUpperCase()
  this.setState({gameKey: this.state.gameKey.toUpperCase()} )
  
  var data = {
    clickPosition: -1,
    game_key: this.state.gameKey,
  };

  sendDataToServer(this, data)

  event.preventDefault();

}

handleGameKeyChange(event) {
  this.setState({gameKey: event.target.value} ) 
}

render() {
  const current = this.state.currentDisplay;
  return (
    // TODO lock scaling of buttons when window width is shrunk
    <div className="game">
      <div className="game-title">
        <h1>Royal Game of Ur</h1> 
      </div>
      <div className="game-board">
        <Board
          squares={current}
          onClick={i => this.handleClick(i)}
        />
      </div>

      <br/>
      <br/>

      <form onSubmit={this.handleGameKeySubmit}>
        <label>
          Game Key: 
          <input type="text" value={this.state.gameKey} onChange={this.handleGameKeyChange } autoCorrect="off" autoCapitalize="none"/>
        </label>
        <input type="submit" value="Submit" />
      </form>

      <text>
        <label>
          Dice Roll: 
          <input type="text" value={this.state.diceRoll} readOnly={true}/>
        </label>
      </text>
    </div>
  );
}
}


// ========================================

//ReactDOM.render(<Game />, document.getElementById("root")); // we get stuck on the loading screen with this 


function sendDataToServer(targetobject, data) {
  const endpointUri = 'hiddenRequest';
  var endpoint = "http://" + window.location.host.toString() + '/' + endpointUri;
  console.log(endpoint);

  var request = new XMLHttpRequest();
  request.open('PUT', endpoint, true);
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  request.onload = function () {
    var gamestate  = JSON.parse(request.responseText);
    targetobject.setState({
      currentDisplay : gamestate["gameState"],
      diceRoll: gamestate["rollValue"],
    })
  }
  request.send(JSON.stringify(data));
}

// dec2hex :: Integer -> String
// i.e. 0-255 -> '00'-'ff'
function dec2hex (dec) {
  return ('0' + dec.toString(16)).substr(-2)
}

// generateId :: Integer -> String
function generateId (len) {
  var arr = new Uint8Array((len || 40) / 2)
  window.crypto.getRandomValues(arr)
  return Array.from(arr, dec2hex).join('')
}

bottlereact._register('Board', Board)
bottlereact._register('Game', Game)
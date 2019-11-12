// DEPRECATED; NOT IN USE
function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

function Square_nb(props) {
return (
  <button className="square_nb" onClick={props.onClick}>
    {props.value}
  </button>
);
}

class Board extends React.Component {
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

render() {
  return (
    <div>
      <div className="board-row">
        {this.renderSquare(0)}
        {this.renderSquare(1)}
        {this.renderSquare(2)}
        {this.renderSquare(3)}
        {this.renderSquare_nb(4)}
        {this.renderSquare_nb(5)}
        {this.renderSquare(6)}
        {this.renderSquare(7)}
      </div>
      <div className="board-row">
        {this.renderSquare(8)}
        {this.renderSquare(9)}
        {this.renderSquare(10)}
        {this.renderSquare(11)}
        {this.renderSquare(12)}
        {this.renderSquare(13)}
        {this.renderSquare(14)}
        {this.renderSquare(15)}
      </div>
      <div className="board-row">
        {this.renderSquare(16)}
        {this.renderSquare(17)}
        {this.renderSquare(18)}
        {this.renderSquare(19)}
        {this.renderSquare_nb(20)}
        {this.renderSquare_nb(21)}
        {this.renderSquare(22)}
        {this.renderSquare(23)}
      </div>
    </div>
  );
}
}

class Game extends React.Component {

constructor(props) {
  super(props);
  this.state = {
    xIsNext: true,
    gameID : 'fffffff',
    currentDisplay : Array(20).fill(null)
  };
}

handleClick(i) {
  const newState = this.state.currentDisplay.slice();
  newState[i] = this.state.xIsNext ? "X" : "O";
  this.state.xIsNext = !this.state.xIsNext;
  this.setState({
    currentDisplay : newState
  })
}

render() {
  const current = this.state.currentDisplay;

  status = 'Some shit'

  return (
    <div className="game">
      <div className="game-board">
        <Board
          squares={current}
          onClick={i => this.handleClick(i)}
        />
      </div>
    </div>
  );
}
}


// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));


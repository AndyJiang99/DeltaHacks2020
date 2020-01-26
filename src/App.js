import React from 'react';
import logo from './logo.svg';

import {
  Button, Modal, Dialog, TextField, Card, CardContent, CardActions, Typography
} from '@material-ui/core';

import './App.scss';
import NewTaskMenu from './NewTaskMenu';
import UnsetTask from './UnsetTask';
import NewFixedMenu from './NewFixedMenu';
import Timeline from './Timeline';

let id = 1;
export default class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      schedOpen: false,
      fixedOpen: false,
      schedTasks: [],
      fixedTasks: [],
      submitted: false, 
      promptOpen: true,
      sentiment_message: null
    };
  }

  onCancel = () => {
    this.setState({
      schedOpen: false,
      fixedOpen: false
    })
  }

  onCreateSchedulable = (data) => {
    this.onCancel();

    if(Object.keys(data)){
      this.state.schedTasks.push({
        id: id++,
        ...data
      });
      this.setState({
        schedTasks: this.state.schedTasks.slice()
      });
    }
    
  }

  onCreateFixed = data => {
    this.onCancel();

    this.state.fixedTasks.push({
      id: id++,
      ...data
    });
    this.setState({
      schedTasks: this.state.schedTasks.slice()
    })
  }
  handleCreateSchedClick = () => {
    this.setState({
      schedOpen: true
    })
  }

  handleCreateFixedClick = () => {
    this.setState({
      fixedOpen: true
    })
  }

  render(){
    return (
      <div className="App">
        <Typography variant="h1">MoodViewed</Typography>
        <div className="buttons-header">
          <Button variant="contained" onClick={this.handleCreateSchedClick}>Add Schedulable Task</Button>
          <Button variant="contained" onClick={this.handleCreateFixedClick}>Add Fixed Task</Button>
          <Button variant="contained" color="primary" onClick={() => this.setState({submitted: true, runningSample: false})}>Create Schedule</Button>
          <Button variant="outlined" onClick={() => this.setState({submitted: true, runningSample: true})}>Use sample</Button>
        </div>
        <Dialog open={this.state.promptOpen}>
          <Card className="promptDialog">
            <CardContent className="promptDialog-content">
              <h3>How are you feeling today?</h3>
              <TextField variant="outlined" multiline rows={5}
              onChange={e => this.setState({sentiment_message: e.target.value || null})} />
            </CardContent>
            <CardActions>
              <Button variant="outlined" onClick={() => this.setState({promptOpen: false})}>Submit</Button>
            </CardActions>
            
          </Card>
        </Dialog>
        <NewTaskMenu
        open={this.state.schedOpen}
        onSubmit={this.onCreateSchedulable}
        onCancel={this.onCancel}
        />
        <NewFixedMenu
        open={this.state.fixedOpen}
        onSubmit={this.onCreateFixed}
        onCancel={this.onCancel}
        />
        <div className="tasksListContainer">
          <div className="tasksListColumn">
            <h3>Schedulable Tasks</h3>
            <div className="tasksList">
              {this.state.schedTasks.map(task => <UnsetTask {...task} key={task.id} />) || 'none'}
            </div>
            
          </div>
          <div className="tasksListColumn">
            <h3>Fixed Tasks</h3>
            <div className="tasksList">
              {this.state.fixedTasks.map(task => <UnsetTask {...task} key={task.id} />) || 'none'}
            </div>
            
          </div>
        </div>
        
        {this.state.submitted && <Timeline runningSample={this.state.runningSample} schedTasks={this.state.schedTasks} fixedTasks={this.state.fixedTasks} sentiment_message={this.state.sentiment_message}/>}
      </div>
    );
  }
  
}


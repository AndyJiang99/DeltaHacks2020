import React from 'react';
import { Dialog, Button, Card, CardContent, CardActions, TextField, Slider, Input, Typography } from '@material-ui/core';

import { DateTimePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';

import './NewTaskMenu.scss';
class NewTaskMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      deadline: null,
      difficulty: 1,
      description: ""
    };
  }

  handleDeadlineChange = date => {
      this.setState({
          deadline: date
      });
  }

  handleSliderChange = (e, diff) => {
      this.setState({
          difficulty: diff
      });
  }

  handleDifficultyChange = diff => this.handleSliderChange(undefined, diff)

  handleTimeChange = e => this.setState({est_duration: parseInt(e.target.value)})

  onSubmit = () => {
    const { title, description, est_duration, deadline, difficulty } = this.state;
    
    this.props.onSubmit({
        title,
        description,
        est_duration,
        deadline: deadline.toJSON(),
        difficulty,
        start_time: null,
        end_time: null
    });
    this.setState({
        name: undefined,
        description: "",
        est_duration: undefined,
        deadline: null
    });
  }

  onCancel = () => {
      this.setState({
        name: undefined,
        description: "",
        est_duration: undefined,
        deadline: null
      });
      this.props.onCancel();
  }
  render() {
    return (
        <Dialog
        open={this.props.open}
        >
            <Card className="create-content">
                <CardContent >
                    <h2>New Schedulable Task</h2>
                    <TextField variant="outlined" label="Title" onChange={e => this.setState({title: e.target.value})}/>
                    <TextField variant="outlined" label="Description" multiline rows="5" onChange={e => this.setState({description: e.target.value || ""})}/>
                    <TextField variant="outlined" 
                    label="Estimated Time (minutes)" 
                    type="number"
                    value={String(this.state.est_duration)}
                    onChange={this.handleTimeChange}
                    inputProps={{
                        min: 1,
                    }}/>
                    <MuiPickersUtilsProvider utils={DateFnsUtils}>
                    <DateTimePicker
                        variant="inline"
                        label="Deadline"
                        value={this.state.deadline}
                        onChange={this.handleDeadlineChange}
                        inputVariant="outlined"
                        disablePast
                    />
                    </MuiPickersUtilsProvider>
                    <div className="slider-container">
                        <Typography variant="caption">Difficulty</Typography>
                        <Slider
                        value={this.state.difficulty}
                        min={1}
                        max={10}
                        onChange={this.handleSliderChange}
                        valueLabelDisplay="on"/>
                    </div>
                    
                </CardContent>
                <CardActions className="actions">
                    <Button variant="outlined" color="primary" onClick={this.onSubmit}
                    disabled={!this.state.deadline || this.state.title === undefined || this.state.description === undefined || !this.state.est_duration}>Submit</Button>
                    <Button variant="outlined" color="secondary" onClick={this.onCancel}>Cancel</Button>
                </CardActions>

            </Card>
            
        </Dialog>
    )
  }

}

export default NewTaskMenu;

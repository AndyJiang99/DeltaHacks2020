import React from 'react';
import { Dialog, Button, Card, CardContent, CardActions, TextField, Slider, Typography } from '@material-ui/core';

import { DateTimePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';

import './NewTaskMenu.scss';
class NewFixedMenu extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            title: undefined,
            description: "",
            start_time: null,
            end_time: null
        };
    }
  onSubmit = () => {
    const { title, description, start_time, end_time } = this.state;
    
    this.props.onSubmit({
        title,
        description,
        start_time: start_time.toJSON(),
        end_time: end_time.toJSON()
    });
    this.setState({
        name: undefined,
        description: "",
        start_time: null,
        end_time: null
    });
  }

  onCancel = () => {
      this.setState({
        name: undefined,
        description: "",
        start_time: null,
        end_time: null
      });
      this.props.onCancel();
  }
  render() {
    return (
        <Dialog
        open={this.props.open}
        >
            <Card className="create-content">
                <CardContent>
                    <h2>New Fixed Task</h2>
                    <TextField variant="outlined" label="Title" onChange={e => this.setState({title: e.target.value})}/>
                    <TextField variant="outlined" label="Description" multiline rows="5" onChange={e => this.setState({description: e.target.value || ""})}/>
                    
                    <MuiPickersUtilsProvider utils={DateFnsUtils}>
                    <DateTimePicker
                        variant="inline"
                        label="Start Time"
                        value={this.state.start_time}
                        onChange={date => this.setState({start_time: date})}
                        inputVariant="outlined"
                        disablePast
                    />
                    <DateTimePicker
                        variant="inline"
                        label="End Time"
                        value={this.state.end_time}
                        onChange={date => this.setState({end_time: date})}
                        inputVariant="outlined"
                        disablePast
                    />
                    </MuiPickersUtilsProvider>
                    
                    
                </CardContent>
                <CardActions className="actions">
                    <Button variant="outlined" color="primary" onClick={this.onSubmit}
                    disabled={!this.state.start_time || !this.state.end_time || this.state.title === undefined}>Submit</Button>
                    <Button variant="outlined" color="secondary" onClick={this.onCancel}>Cancel</Button>
                </CardActions>

            </Card>
            
        </Dialog>
    )
  }

}

export default NewFixedMenu;

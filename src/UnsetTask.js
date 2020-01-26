import React from 'react';
import { Card } from '@material-ui/core';

class UnsetTask extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      someKey: 'someValue'
    };
  }

  render() {
    return (
      <Card>
        <h4>{this.props.title}</h4>
      </Card>
    );
  }

}

export default UnsetTask;

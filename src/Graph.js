import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

class Graph extends Component {
	constructor() {
		super();
	}

	render() {
		return (
			<div id="calculator" style={{ "height": "100%", "width": "100%" }}></div>
		);
	}
}

export default Graph;

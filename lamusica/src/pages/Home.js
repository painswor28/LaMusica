import React, { Component } from "react";
import TrackList from "../components/TrackList";

import axios from "axios";

class Home extends Component {
    state = {
        tracks: []
    }

    componentDidMount() {
        this.resetState();
    }

    getTracks = () => {
        axios.get("http://db8.cse.nd.edu:5003/backend/tracks/").then(res => this.setState({ tracks: res.data['results'] }))
    }

    resetState = () => {
        this.getTracks();
    }

    search = (query) => {
        if (query.key === 'Enter') {
            console.log(query.val)
        }
    }

    render() {
        return (
            <div class="jumbotron">
                <h1 class="display-4">Welcome to <b>La Música</b></h1>
                <br />
                <p class="lead">
                    Built for DJ's by DJ's, at its core <b>La Música</b> is designed to aid music creativity.  With over 500,000 unique songs, La Música delivers high quality music metadata information and makes song suggestions.
                </p>

                <div class="card shadow-lg border-0 rounded-lg mt-0 mb-3">
                    <div class="card-header justify-content-center">
                        <h3 class="font-weight-light my-1 text-center">Here's How it Works:</h3>
                        <div class="row">
                            <div class='col'>
                                <ol>
                                    <b>Choose a dataset</b> <br />
                                    Either use ours of over 500,000 or choose your own spotify playlist
                                    <br /><br />
                                    <b>Search a song</b><br />
                                    And view metadata details
                                    <br /> <br />

                                    <b>Get Recommendations</b>
                                </ol>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="input-group mb-3">
                    <input type='text' className="form-control" placeholder="Search Here" onKeyDown={this.search}></input>
                </div>

                <TrackList
                    tracks={this.state.tracks}
                    resetState={this.resetState}
                />
            </div >

        );
    }
} export default Home;
import React, { Component } from "react";


class Home extends Component {
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
                        <h3 class="font-weight-light my-1 text-center">Two Options</h3>
                        <div class="row">
                            <div class="col">
                                Search for metadata
                                <br />
                                <button href="/search" role="button" class="btn btn-outline-primary">Search</button>
                            </div>
                            <div class="col">
                                Get Recommendations
                                <br />
                                <button href="/search" role="button" class="btn btn-outline-primary">Recommend</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div >

        );
    }
} export default Home;
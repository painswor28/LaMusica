import React, { Component, Fragment } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";

class TrackDetailsModal extends Component {
    state = {
        modal: false
    };

    toggle = () => {
        this.setState(previous => ({
            modal: !previous.modal
        }));
    };

    render() {
        const track = this.props.track
        var button = <button onClick={this.toggle} type="button" className="btn btn-outline-primary">View Details</button>

        return (
            <Fragment>
                {button}

                <Modal isOpen={this.state.modal} toggle={this.toggle}>
                    <ModalHeader toggle={this.toggle}>Song Metadata</ModalHeader>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item"><b>Name: </b>{track.name}</li>
                        <li class="list-group-item"><b>Danceability: </b>{track.danceability}</li>
                        <li class="list-group-item"><b>Energy: </b>{track.energy}</li>
                        <li class="list-group-item"><b>Loudness: </b>{track.loudness}</li>
                        <li class="list-group-item"><b>Speechiness: </b>{track.speechiness}</li>
                        <li class="list-group-item"><b>Danceability: </b>{track.danceability}</li>
                        <li class="list-group-item"><b>Acousticness: </b>{track.acousticness}</li>
                        <li class="list-group-item"><b>Liveness: </b>{track.liveness}</li>
                        <li class="list-group-item"><b>Valence: </b>{track.valence}</li>
                        <li class="list-group-item"><b>Tempo: </b>{track.tempo}</li>
                        <li class="list-group-item"><b>Key: </b>{track.camelot_key}</li>
                        <li class="list-group-item"><b>Time Signature: </b>{track.time_signature}</li>
                        <li class="list-group-item"><b>Popularity: </b>{track.popularity}</li>
                    </ul>
                </Modal>
            </Fragment>
        )
    }
}

export default TrackDetailsModal;
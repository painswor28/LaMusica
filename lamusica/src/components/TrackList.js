import React, { Component } from "react";
import { Table } from "reactstrap";

import TrackDetailsModal from "./TrackDetailsModal";

class TrackList extends Component {
    render() {
        const tracks = this.props.tracks;
        return (
            <Table light>
                <thead>
                    <tr>
                        <th>Song Name</th>
                        <th>Artists</th>
                        <th>Key</th>
                        <th>Tempo</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {!tracks || tracks.length <= 0 ? (
                        <tr>
                            <td colSpan="6" align="center">
                                <b>Sorry, we don't have any matching songs yet.</b>
                            </td>
                        </tr>
                    ) : (
                        tracks.map(track => (
                            <tr key={track.uri}>
                                <td>{track.name}</td>
                                <td>{track.artists}</td>
                                <td>{track.camelot_key}</td>
                                <td>{Math.round(track.tempo)} BPM</td>
                                <td><TrackDetailsModal track={track} /></td>
                                <td><button className="btn btn-outline-danger" type="button">Recommend</button></td>
                            </tr>
                        ))
                    )}
                </tbody>
            </Table>
        );
    }
}

export default TrackList;
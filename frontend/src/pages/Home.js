import React, { Component } from "react";
import { Helmet } from 'react-helmet-async';
import axios from "axios"
import ReactAudioPlayer from 'react-audio-player';
import SpotifyWebApi from 'spotify-web-api-js';

import {
    Box,
    Modal,
    CardHeader,
    Link,
    Card,
    Table,
    Stack,
    Avatar,
    Button,
    Slider,
    Checkbox,
    TableRow,
    TableBody,
    TableCell,
    Container,
    Typography,
    CircularProgress,
    LinearProgress,
    TableContainer,
    TablePagination,
    CardContent, List, ListItem
} from '@mui/material';

import PlaylistList from "../components/PlaylistList";
import Scrollbar from '../components/scrollbar';
import Searchbar from "../components/SearchBar";
import DetailGraph from "../components/DetailGraph";
import FilterToolbar from "../components/FilterToolbar";

import UserListHead from '../components/UserListHead';
import UserListToolbar from '../components/UserListToolbar'

const API_URL = "http://db8.cse.nd.edu:5003/backend/";

const TABLE_HEAD = [
    { id: 'avatar', label: '' },
    { id: 'name', label: 'Song Name', alignRight: false },
    { id: 'artistis', label: 'Artists', alignRight: false },
    { id: 'key', label: 'Song Key', alignRight: false },
    { id: 'tempo', label: 'Tempo', alignRight: false },
    { id: 'preview', label: 'Preview', alignRight: false },
];

const CHART_OPTIONS = {
    stroke: { width: 2 },
    fill: { opacity: 0.48 },
    xaxis: {
        categories: ['Danceability', 'Energy', 'Acousticness', 'Liveness', 'Valence'],
    },
}

const spotifyApi = new SpotifyWebApi();

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            tracks: [],
            selected_tracks: [],
            tracks_loading: false,
            isTrackSelected: false,
            trackDetail: {},

            playlists: [],
            playlist_search_query: '',
            selected_playlists: [],
            loading_playlists: false,
            loading_playlist: false,
            playlist_loaded: false,
            isPlaylistSelected: false,


            numTracks: 0,
            numSelected: 0,
            page: 0,
            search_query: '',

            recommendFilter: '',
            recommendDataset: 0,
            isLoadingRecommendations: false,
            recommended_tracks: [],

            open: false,
            datasets: [{
                value: 0,
                label: 'Database'
            }],

            series: [],
        };
    }

    componentDidMount() {
        this.resetState();
    }

    resetState = () => {
        this.getTracks();
    }

    getTracks = () => {
        console.log(this.state.search_query)
        this.setState({ tracks_loading: true })
        axios.get(`${API_URL}results/?page=${this.state.page + 1}&search=${this.state.search_query}`).then(res => this.setState({
            tracks: res.data.results,
            numSelected: res.data.count,
            numTracks: res.data.count,
            selected_tracks: res.data.results,
            tracks_loading: false,
        }))
    }

    handleSelectTrack = (event, track) => {
        const tracks = this.state.tracks;
        const numTracks = this.state.numTracks;
        if (event.target.checked) {
            this.setState({ selected_tracks: [track], isTrackSelected: true, numSelected: 1 })
        } else {
            this.setState({ selected_tracks: tracks, isTrackSelected: false, numSelected: numTracks })
        }
    }

    handleChangePage = (event, newPage) => {
        this.setState({ page: newPage, selected_tracks: [] }, () => { this.getTracks(); })
    }

    handleSearch = (event) => {
        if (event.key === "Enter") {
            console.log('searching...')
            const data = { "query": event.target.value }
            this.setState({ page: 0, search_query: event.target.value, selected_tracks: [], numSelected: 0 }, () => { axios.post(`${API_URL}search/add/`, data).then(() => this.getTracks()) })
        }
    }

    handlePlaylistSearch = (event) => {
        if (event.key === "Enter") {
            console.log(event.target.value)
            this.setState({ playlist_search_query: event.target.value }, () => { this.getPlalists(); })
        }
    }

    getPlalists = () => {
        const data = { "username": this.state.playlist_search_query };
        this.setState({ loading_playlists: true })
        axios.post(`${API_URL}user/playlists/`, data).then(response => this.setState({
            playlists: response.data,
            selected_playlists: response.data,
            loading_playlists: false
        }))
    }

    selectPlaylist = (event, param) => {
        if (this.state.loading_playlist) {
            return
        }
        const playlists = this.state.playlists
        const selected = this.state.isPlaylistSelected
        console.log(param.uri)
        if (!selected) {
            this.setState({
                selected_playlists: [param],
                isPlaylistSelected: !selected,
                loading_playlist: true,
                datasets: [{
                    value: 0,
                    label: 'Database'
                },
                {
                    value: param.uri,
                    label: param.name
                }]
            }, () => { this.loadPlaylist(param); })
        } else {
            this.setState({
                selected_playlists: playlists,
                isPlaylistSelected: !selected,
                playlist_loaded: false,
                datasets: [{
                    value: 0,
                    label: 'Database'
                }]
            })
        }
    }

    loadPlaylist = (param) => {

        console.log(param.uri)
        const data = { "uri": param.uri }

        axios.post(`${API_URL}user/playlists/add/`, data).then(response => this.setState({
            playlist_loaded: true,
            loading_playlist: false
        }))
    }

    handleOpen = (track, recommend) => {
        const selectedTrack = this.state.selected_tracks[0];
        console.log(selectedTrack)

        if (recommend) {
            this.setState({
                series: [
                    { name: track.name, data: [track.danceability, track.energy, track.acousticness, track.liveness, track.valence] },
                    { name: selectedTrack.name, data: [selectedTrack.danceability, selectedTrack.energy, selectedTrack.acousticness, selectedTrack.liveness, selectedTrack.valence] },
                ],
                open: true,
                trackDetail: track
            })
        } else {
            this.setState({
                series: [
                    { name: track.name, data: [track.danceability, track.energy, track.acousticness, track.liveness, track.valence] },
                ],
                open: true,
                trackDetail: track
            })
        }
    }

    handleClose = () => {
        this.setState({ open: false })
    }

    handleDatasetSelect = (dataset) => {
        console.log(dataset.target.value)
        this.setState({ recommendDataset: dataset.target.value })
    }

    handleFilterSelect = (filter) => {
        console.log(filter.target.value)
        this.setState({ recommendFilter: filter.target.value })
    }

    handleRecommend = () => {
        if (this.state.selected_tracks.length !== 1) {
            alert('Please select a seed song in step 1')
            return
        }
        console.log(this.state.recommendDataset)
        console.log(this.state.recommendFilter)

        const selectedTrack = this.state.selected_tracks[0].uri;
        const selectedDataset = this.state.recommendDataset;
        const selectedFilter = this.state.recommendFilter;

        this.setState({ isLoadingRecommendations: true, recommended_tracks: [] });
        const data = {
            "uri": selectedTrack,
            "dataset": selectedDataset,
            "measure": selectedFilter,
        };
        axios.post(`${API_URL}recommend/`, data).then(res => this.setState({
            recommended_tracks: res.data,
            isLoadingRecommendations: false,
        }))

    }

    render() {
        return (
            <div>
                <Helmet>
                    <title>LaMúsica</title>
                </Helmet>
                <Container>
                    <Typography variant="h1" sx={{ m: 3 }}>
                        Welcome to LaMúsica
                    </Typography>
                    <Typography variant="h4" sx={{ m: 3 }}>
                        Built for DJ's by DJ's, at its core La Música is designed to aid music creativity. With over 1,000,000 unique songs, La Música delivers high quality music metadata information and makes song suggestions.
                    </Typography>
                </Container>

                <Container>
                    <Stack direction="row" alignItems="center" justifyContent="space-between" mb={5}>
                        <Typography variant="h4" gutterBottom>
                            1. Select Song
                        </Typography>
                    </Stack>

                    <Card>
                        <UserListToolbar numSelected={this.state.isTrackSelected} filterName={this.props.search_query} onFilterName={this.handleSearch} />

                        <Scrollbar>
                            <TableContainer sx={{ minWidth: 800 }}>
                                <Table>
                                    <UserListHead
                                        headLabel={TABLE_HEAD}
                                    />
                                    <TableBody>
                                        {this.state.tracks_loading && (
                                            <TableRow>
                                                <TableCell colSpan={7}>
                                                    <LinearProgress />
                                                </TableCell>
                                            </TableRow>
                                        )}
                                        {this.state.selected_tracks.map((track, index) => {
                                            return (
                                                <>
                                                    <TableRow hover key={index}>
                                                        <TableCell padding="checkbox">
                                                            <Checkbox checked={this.state.isTrackSelected} onChange={(event) => this.handleSelectTrack(event, track)} />
                                                        </TableCell>

                                                        <TableCell component="th" scope="row" padding="none"><Avatar alt={track.name} src={track.album.cover_image} /></TableCell>

                                                        <TableCell>

                                                            <Button onClick={() => this.handleOpen(track)}>{track.name}</Button>

                                                        </TableCell>
                                                        <TableCell align="left">{track.artists.map(artist => artist).join(', ')}</TableCell>

                                                        <TableCell align="left">{track.camelot_key}</TableCell>

                                                        <TableCell align="left">{Math.round(track.tempo)} BPM</TableCell>

                                                        <TableCell alight="left">
                                                            {track.preview_url ? (
                                                                <ReactAudioPlayer src={track.preview_url} controls style={{ height: 32 }} />
                                                            ) : (
                                                                <ReactAudioPlayer src={''} controls style={{ height: 32 }} />
                                                            )}
                                                        </TableCell>
                                                    </TableRow>
                                                </>
                                            );
                                        })}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Scrollbar>
                        <TablePagination
                            rowsPerPageOptions={[10]}
                            component="div"
                            count={this.state.numSelected}
                            rowsPerPage={10}
                            page={this.state.page}
                            onPageChange={this.handleChangePage}
                        />
                    </Card>
                </Container>

                <Container>
                    <Typography variant="h4" sx={{ mb: 5, mt: 8 }}>
                        2. Select Playlist
                    </Typography>

                    <Searchbar
                        filterName={this.props.playlist_search_query}
                        onFilterName={this.handlePlaylistSearch}
                        placeholder='Spotify Username...'
                    />


                    <Box sx={{ m: 3 }} />
                    {this.state.loading_playlists ? (
                        <Box align='center' sx={{ display: 'flex' }}>
                            <CircularProgress />
                        </Box>
                    ) : (
                        <PlaylistList playlists={this.state.selected_playlists} onSelect={this.selectPlaylist} loading={this.state.loading_playlist} loaded={this.state.playlist_loaded} />
                    )}
                </Container>


                <Container>
                    <Typography variant="h4" sx={{ mb: 5, mt: 8 }}>
                        3. Get Recommendations
                    </Typography>

                    <Card>
                        <FilterToolbar recommend={this.handleRecommend} datasets={this.state.datasets} selectDataset={this.handleDatasetSelect} selectFilter={this.handleFilterSelect} />
                        <Scrollbar>
                            <TableContainer sx={{ minWidth: 800 }}>
                                <Table>
                                    <UserListHead
                                        headLabel={TABLE_HEAD}
                                    />
                                    <TableBody>
                                        {this.state.isLoadingRecommendations && (
                                            <TableRow>
                                                <TableCell colSpan={7}>
                                                    <LinearProgress />
                                                </TableCell>
                                            </TableRow>
                                        )}
                                        {this.state.recommended_tracks.map((track, index) => {
                                            return (
                                                <>
                                                    <TableRow hover key={index}>
                                                        <TableCell><Checkbox style={{ display: "none" }}>dagds</Checkbox></TableCell>

                                                        <TableCell component="th" scope="row" padding="none"><Avatar alt={track.name} src={track.album.cover_image} /></TableCell>

                                                        <TableCell>

                                                            <Button onClick={() => this.handleOpen(track, true)}>{track.name}</Button>

                                                        </TableCell>
                                                        <TableCell align="left">{track.artists.map(artist => artist).join(', ')}</TableCell>

                                                        <TableCell align="left">{track.camelot_key}</TableCell>

                                                        <TableCell align="left">{Math.round(track.tempo)} BPM</TableCell>

                                                        <TableCell alight="left"><ReactAudioPlayer src={track.preview_url} controls style={{ height: 32 }} /></TableCell>
                                                    </TableRow>
                                                </>
                                            );
                                        })}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Scrollbar>

                    </Card>

                </Container>

                <Modal open={this.state.open} onClose={this.handleClose} aria-labelledby="parent-modal-title">
                    <Card style={{ margin: "auto", display: "block", width: "600px", marginTop: "80px" }}>
                        <CardHeader
                            title={this.state.trackDetail.name}
                            subheader={this.state.trackDetail.artists}
                        />

                        <CardContent>
                            Popularity
                            <Slider
                                defaultValue={this.state.trackDetail.popularity}
                                disabled
                                valueLabelDisplay="on"
                                marks={[
                                    { value: 0, label: '0' },
                                    { value: 100, label: '100' }
                                ]}
                            />
                            <Typography>
                                Song Metadata
                            </Typography>
                            <DetailGraph track={this.state.trackDetail} series={this.state.series} />
                            <List>
                                <ListItem>
                                    Key: {this.state.trackDetail.camelot_key}
                                </ListItem>
                                <ListItem>
                                    Tempo: {this.state.trackDetail.tempo}
                                </ListItem>
                            </List>
                            <Button onClick={this.handleClose}>Close</Button>
                        </CardContent>
                    </Card>
                </Modal>
            </div>
        )
    }
}
export default Home;
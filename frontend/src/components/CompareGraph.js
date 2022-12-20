import React from 'react';
import { Modal, Button, Link } from '@mui/material';
import ReactApexCharts from 'react-apexcharts';

import { useTheme, styled } from '@mui/material/styles';

import { useChart } from './chart';

function DetailGraph({ track }) {

    const theme = useTheme();
    const CHART_HEIGHT = 392;

    const LEGEND_HEIGHT = 72;

    const [open, setOpen] = React.useState(false);

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const series = [
        { name: track.name, data: [track.danceability, track.energy, track.acousticness, track.liveness, track.valence] },
    ];

    const chartLabels = ['Danceability', 'Energy', 'Acousticness', 'Liveness', 'Valence'];


    const chartOptions = useChart({
        stroke: { width: 2 },
        fill: { opacity: 0.48 },
        legend: { floating: true, horizontalAlign: 'center' },
        xaxis: {
            categories: ['Danceability', 'Energy', 'Acousticness', 'Liveness', 'Valence'],
            labels: {
                style: {
                    colors: [...Array(6)].map(() => theme.palette.text.secondary),
                },
            },
        },
        yaxis: {
            min: 0,
            max: 1,
            tickAmount: 4,
        }
    });

    return (
        <div>
            <ReactApexCharts type='radar' options={chartOptions} series={series} />
        </div>
    );
};

export default DetailGraph;
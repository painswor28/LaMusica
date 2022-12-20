import PropTypes from 'prop-types';
// @mui
import { styled, alpha } from '@mui/material/styles';
import { Toolbar, MenuItem, TextField, Box, Button } from '@mui/material';


// ----------------------------------------------------------------------

const StyledRoot = styled(Toolbar)(({ theme }) => ({
  height: 96,
  display: 'flex',
  justifyContent: 'space-between',
  padding: theme.spacing(0, 1, 0, 3),
}));

const filterOptions = [
  {
    value: 'cam_dance',
    label: 'Danceability'
  },
  {
    value: 'cam_dance_energy',
    label: 'Danceability & Energy'
  },
  {
    value: 'cam_dance_energy_valence',
    label: 'Dance, Energy, & Valence'
  },
];

// ----------------------------------------------------------------------

export default function FilterToobar({ recommend, datasets, selectDataset, selectFilter }) {
  return (
    <StyledRoot>
      <Box
        component="form"
        sx={{
          '& .MuiTextField-root': { m: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        <TextField
          id="outlined-select"
          select
          label="dataset"
          helperText="Please select your dataset"
          onChange={selectDataset}
        >
          {datasets.map((dataset) => (
            <MenuItem key={dataset.value} value={dataset.value}>
              {dataset.label}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          id="outlined-select"
          select
          label="filter"
          helperText="Please select your filter criteria"
          onChange={selectFilter}
        >
          {filterOptions.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
            </MenuItem>
          ))}
        </TextField>
      </Box>
      <Button variant='contained' onClick={() => recommend()}>Run Algorithm</Button>
    </StyledRoot>
  );
}

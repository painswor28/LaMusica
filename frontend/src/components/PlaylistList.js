import PropTypes from 'prop-types';

import { Grid, Box, Card, Link, Typography, Stack, Button } from '@mui/material';
import { styled } from '@mui/material/styles';

// ----------------------------------------------------------------------
const StyledProductImg = styled('img')({
  top: 0,
  width: '100%',
  height: '100%',
  objectFit: 'cover',
  position: 'absolute',
});


PlaylistList.propTypes = {
  playlists: PropTypes.array.isRequired,
  onSelect: PropTypes.func,
};

export default function PlaylistList({ playlists, onSelect, loading, loaded, ...other }) {
  return (

    <Grid container spacing={3} {...other}>
      {playlists.map((playlist) => (
        <Grid key={playlist.uri} item xs={12} sm={6} md={3}>
          <Card>
            <Box sx={{ pt: '100%', position: 'relative' }}>
              <StyledProductImg alt={playlist.name} src={playlist.image} />
            </Box>

            <Stack spacing={2} sx={{ p: 3 }}>
              <Link color="inherit" underline="hover" onClick={(event) => onSelect(event, playlist)}>
                <Typography variant="subtitle2" noWrap>
                  {playlist.name}
                </Typography>
              </Link>

              <Stack direction="row" alignItems="center" justifyContent="space-between">
                <Typography variant="subtitle1">
                  {playlist.num_followers} Followers
                </Typography>
              </Stack>

              <Button variant="outlined" onClick={(event => onSelect(event, playlist))}>{loading ? ('loading...') : (loaded ? 'loaded' : 'load')}</Button>
            </Stack>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
}

import { Box, Grid, Container, Text, Spinner } from "@chakra-ui/react"
import Navbar from "@/components/Navbar"
import Hero from "@/components/Hero"
import PlaceCard from "@/components/PlaceCard"
import SearchBar from "@/components/SearchBar"
import { useState, useEffect } from "react"
import axios from "axios"


export default function Home() {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  // Fetch places data when the component mounts
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/v1/places/")
      .then((response) => {
        setPlaces(response.data); 
        setLoading(false); 
      })
      .catch((err) => {
        setError("Error fetching places data");
        setLoading(false); 
      });
  }, []);

  // Filter places based on the search term
  const filteredPlaces = places.filter(
    (place) =>
      place.title?.toLowerCase().includes(search.toLowerCase()) ||
      place.description?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <Box textAlign="center" mt={10}>
        <Spinner size="xl" />
        <Text mt={4}>Loading...</Text>
      </Box>
    );
  }

  if (error) {
    return (
      <Box textAlign="center" mt={10}>
        <Text color="red.500">{error}</Text>
      </Box>
    );
  }

  return (
    <Box>
      <Navbar />
      <Hero />
      <Container maxW="6xl" py={10}>
        <SearchBar value={search} onChange={(e) => setSearch(e.target.value)} />
        <Grid templateColumns={{ base: "1fr", md: "repeat(3, 1fr)" }} gap={6}>
          {filteredPlaces.length > 0 ? (
            filteredPlaces.map((place) => (
              <PlaceCard
              key={place.id}
              id={place.id} 
              title={place.title}
              description={place.description}
              imageUrl={place.imageUrl}
              />
            ))
          ) : (
            <Text>No places found for your search.</Text>
          )}
        </Grid>
      </Container>
    </Box>
  );
}
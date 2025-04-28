import { Box, Heading, Text, Button, Stack } from "@chakra-ui/react"
import Link from "next/link"

export default function Hero() {
  return (
    <Box bg="blue.50" py={20} px={6} textAlign="center">
      <Heading fontSize="4xl" mb={4}>Find your next place to stay</Heading>
      <Text fontSize="lg" mb={6}>Browse amazing homes and experiences across the world</Text>
      <Stack direction="row" justify="center" spacing={4}>
        <Link href="/places"><Button colorScheme="blue">Explore Places</Button></Link>
        <Link href="/places/new"><Button variant="outline">List Your Place</Button></Link>
      </Stack>
    </Box>
  )
}
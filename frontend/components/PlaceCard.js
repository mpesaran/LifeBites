import { Box, Image, Heading, Text, Link } from "@chakra-ui/react"
import NextLink from 'next/link'

export default function PlaceCard({ id, title, description, imageUrl }) {
  return (
    <NextLink href={`/places/${id}`} passHref>
      <Link _hover={{ textDecoration: "none" }}>
        <Box
          borderWidth="1px"
          borderRadius="lg"
          overflow="hidden"
          _hover={{ boxShadow: "lg", cursor: "pointer" }}
        >
          <Image src={imageUrl} alt={title} objectFit="cover" width="300px" height="200px" />
          <Box p="6">
            <Heading size="md">{title}</Heading>
            <Text mt={2} noOfLines={2}>
              {description}
            </Text>
          </Box>
        </Box>
      </Link>
    </NextLink>
  )
}

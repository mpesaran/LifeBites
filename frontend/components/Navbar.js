import { Box, Flex, HStack, Button, Text } from "@chakra-ui/react"
import Link from "next/link"

export default function Navbar() {
  return (
    <Box bg="gray.100" px={4} py={3} boxShadow="sm">
      <Flex justify="space-between" align="center" maxW="6xl" mx="auto">
        <Link href="/">
          <Text fontWeight="bold" fontSize="xl">HBnB</Text>
        </Link>
        <HStack spacing={4}>
          <Link href="/places/add"><Button variant="ghost">Add Place</Button></Link>
          <Link href="/signup" passHref><Button colorScheme="blue">Sign Up</Button></Link>
          <Link href="/login"><Button>Login</Button></Link>
        </HStack>
      </Flex>
    </Box>
  )
}
import { Paper, Group, Box, Text, Badge } from "@mantine/core";
import type { Policy } from "../../types";

interface Props {
  policy: Policy;
  color?: string;
}

export default function PolicyCard({ policy, color = "blue" }: Props) {
  return (
    <Paper withBorder p="sm">
      <Group justify="space-between">
        <Box>
          <Text size="sm" fw={500}>{policy.name}</Text>
          <Text size="xs" c="dimmed">{policy.description}</Text>
        </Box>
        <Badge size="sm" variant="light" color={color}>
          {policy.system}
        </Badge>
      </Group>
    </Paper>
  );
}

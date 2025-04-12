import {
  ConversationsList,
  ConversationListSchema,
  ConversationSummariesList,
  ConversationSummaryListSchema,
  ConversationClustersList,
  ConversationClusterListSchema,
} from "@/types/kura";

export const parseConversationFile = async (
  file: File
): Promise<ConversationsList | null> => {
  try {
    const text = await file.text();
    const conversations = JSON.parse(text);
    const parsedConversations = ConversationListSchema.safeParse(conversations);
    if (!parsedConversations.success) {
      console.error(
        "Error parsing conversation file",
        parsedConversations.error
      );
      return null;
    }
    return parsedConversations.data;
  } catch (error) {
    console.error("Error parsing conversation file", error);
    return null;
  }
};

export const parseConversationSummaryFile = async (
  file: File
): Promise<ConversationSummariesList | null> => {
  try {
    const text = await file.text();
    const lines = text.split("\n").filter((line) => line.trim() !== "");
    const summaries = lines.map((line) => JSON.parse(line));

    const parsedSummaries = ConversationSummaryListSchema.safeParse(summaries);
    if (!parsedSummaries.success) {
      console.error(
        "Error parsing conversation summary file",
        parsedSummaries.error
      );
      return null;
    }
    return parsedSummaries.data;
  } catch (error) {
    console.error("Error parsing conversation summary file", error);
    return null;
  }
};

export const parseConversationClusterFile = async (
  file: File
): Promise<ConversationClustersList | null> => {
  try {
    const text = await file.text();
    const lines = text.split("\n").filter((line) => line.trim() !== "");
    const clusters = lines.map((line) => JSON.parse(line));

    const parsedClusters = ConversationClusterListSchema.safeParse(clusters);
    if (!parsedClusters.success) {
      console.error(
        "Error parsing conversation cluster file",
        parsedClusters.error
      );
      return null;
    }
    return parsedClusters.data;
  } catch (error) {
    console.error("Error parsing conversation cluster file", error);
    return null;
  }
};

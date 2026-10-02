// Reasoning: Section 6 ke saare 9 steps ka data ek jagah — taakay
// wizard component khud "dumb" rahe, sirf is config ko render kare

export interface WizardStepConfig {
  key: keyof import("./types").VideoBrief;
  title: string;
  question: string;
  type: "select" | "text" | "textarea" | "number";
  options?: string[];
  optional?: boolean;
}

export const WIZARD_STEPS: WizardStepConfig[] = [
  {
    key: "sector",
    title: "Sector",
    question: "Which sector is this video for?",
    type: "select",
    options: [
      "adult_care", "early_years", "fostering", "childrens_homes",
      "education", "childrens_social_work", "adult_social_work",
      "leaving_care", "other",
    ],
  },
  {
    key: "country",
    title: "Country",
    question: "Which country is this for?",
    type: "select",
    options: ["United Kingdom", "United States", "Australia", "Canada", "UAE", "Saudi Arabia"],
  },
  {
    key: "audience",
    title: "Audience",
    question: "Who is the audience?",
    type: "select",
    options: ["Employees", "Managers", "Customers", "Learners", "Parents", "Professionals", "General public"],
  },
  {
    key: "tone",
    title: "Tone",
    question: "What tone should the video have?",
    type: "select",
    options: ["Professional", "Friendly", "Reassuring", "Inspirational", "Serious", "Educational", "Conversational", "Energetic"],
  },
  {
    key: "culture",
    title: "Culture",
    question: "Any specific cultural requirements? (optional)",
    type: "text",
    optional: true,
  },
  {
    key: "video_type",
    title: "Video Type",
    question: "What type of video is this?",
    type: "select",
    options: ["Training", "Advice", "Marketing", "Help/Support", "Social Media", "Explainer", "Announcement"],
  },
  {
    key: "video_format",
    title: "Format",
    question: "Which video format do you need?",
    type: "select",
    options: ["16:9", "9:16", "1:1"],
  },
  {
    key: "duration_seconds",
    title: "Duration",
    question: "How long should the video be (in seconds)?",
    type: "number",
  },
  {
    key: "description",
    title: "Description",
    question: "Describe the video you would like us to create.",
    type: "textarea",
  },
];

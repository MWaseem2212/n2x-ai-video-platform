import { z } from "zod";

// Reasoning: Ye Zod schema humare Python VideoBrief Pydantic model ka
// TypeScript-equivalent hai — same validation rules, dusri language mein
export const videoBriefSchema = z.object({
  sector: z.enum([
    "adult_care", "early_years", "fostering", "childrens_homes",
    "education", "childrens_social_work", "adult_social_work",
    "leaving_care", "other",
  ]),
  country: z.string().min(1, "Country is required"),
  audience: z.string().min(1, "Audience is required"),
  tone: z.string().min(1, "Tone is required"),
  culture: z.string().optional(),
  video_type: z.string().min(1, "Video type is required"),
  video_format: z.string().min(1),
  duration_seconds: z.coerce.number().min(5, "Minimum 5 seconds").max(300, "Maximum 300 seconds"),
  description: z.string().min(10, "Please describe the video in more detail"),
});

export type VideoBriefFormData = z.infer<typeof videoBriefSchema>;

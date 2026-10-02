"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { videoBriefSchema, type VideoBriefFormData } from "@/lib/schema";
import { WIZARD_STEPS } from "@/lib/wizard-config";
import { createVideo } from "@/lib/api";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function WizardForm() {
  const router = useRouter();
  const [stepIndex, setStepIndex] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const form = useForm<VideoBriefFormData>({
    resolver: zodResolver(videoBriefSchema) as any,
  });

  const currentStep = WIZARD_STEPS[stepIndex];
  const progressPercent = ((stepIndex + 1) / WIZARD_STEPS.length) * 100;
  const isLastStep = stepIndex === WIZARD_STEPS.length - 1;

  async function handleNext() {
    if (!currentStep.optional) {
      const isValid = await form.trigger(currentStep.key);
      if (!isValid) return;
    }

    if (isLastStep) {
      await handleSubmit();
    } else {
      setStepIndex((i) => i + 1);
    }
  }

  async function handleSubmit() {
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const data = form.getValues();
      const result = await createVideo(data);

      sessionStorage.setItem("latest_video_result", JSON.stringify(result));
      router.push("/results");
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleBack() {
    setStepIndex((i) => Math.max(0, i - 1));
  }

  function renderInput() {
    switch (currentStep.type) {
      case "select":
        return (
          <Controller
            control={form.control}
            name={currentStep.key}
            render={({ field }) => (
              <Select onValueChange={field.onChange} value={(field.value as string) ?? ""}>
                <SelectTrigger className="w-full h-11 bg-white border border-gray-300 rounded-lg px-3 py-2 text-gray-800 shadow-sm focus:ring-2 focus:ring-[#1F8C8C] focus:border-[#1F8C8C] transition-all">
                  <SelectValue placeholder="Select an option" />
                </SelectTrigger>
                <SelectContent sideOffset={4} className="bg-white border border-gray-200 shadow-xl rounded-lg z-50">
                  {currentStep.options?.map((opt) => (
                    <SelectItem key={opt} value={opt} className="cursor-pointer hover:bg-[#F4F6F8] hover:text-[#1F8C8C] p-2.5 transition-colors">
                      {opt.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            )}
          />
        );

      case "textarea":
        return (
          <Textarea
            {...form.register(currentStep.key)}
            placeholder="Type your answer..."
            rows={5}
            className="w-full bg-white border border-gray-300 rounded-lg p-3 text-gray-800 shadow-sm focus:ring-2 focus:ring-[#1F8C8C] focus:border-[#1F8C8C] transition-all"
          />
        );

      case "number":
        return (
          <Input
            type="number"
            {...form.register(currentStep.key)}
            placeholder="e.g. 60"
            className="w-full h-11 bg-white border border-gray-300 rounded-lg px-3 text-gray-800 shadow-sm focus:ring-2 focus:ring-[#1F8C8C] focus:border-[#1F8C8C] transition-all"
          />
        );

      default:
        return (
          <Input
            {...form.register(currentStep.key)}
            placeholder="Type your answer..."
            className="w-full h-11 bg-white border border-gray-300 rounded-lg px-3 text-gray-800 shadow-sm focus:ring-2 focus:ring-[#1F8C8C] focus:border-[#1F8C8C] transition-all"
          />
        );
    }
  }

  const currentError = form.formState.errors[currentStep.key];

  return (
    <div className="min-h-screen bg-[#F4F6F8] flex items-center justify-center p-4">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        
        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#1F8C8C]">
              Step {stepIndex + 1} of {WIZARD_STEPS.length}
            </span>
            <span className="text-xs font-medium text-gray-500">
              {Math.round(progressPercent)}% Completed
            </span>
          </div>
          <Progress value={progressPercent} className="h-2 bg-gray-100 rounded-full [&>div]:bg-[#1F8C8C]" />
        </div>

        {/* Title & Description */}
        <h2 className="text-2xl font-bold text-[#1A2B4C] mb-1">
          {currentStep.title}
        </h2>
        <Label className="block text-sm font-normal text-gray-600 mb-6">
          {currentStep.question}
        </Label>

        {/* Input Field */}
        <div className="mb-4">{renderInput()}</div>

        {/* Error Messages */}
        {currentError && (
          <p className="text-sm font-medium text-red-500 mb-4 bg-red-50 p-2.5 rounded-lg border border-red-100">
            {currentError.message as string}
          </p>
        )}

        {submitError && (
          <p className="text-sm font-medium text-red-500 mb-4 bg-red-50 p-2.5 rounded-lg border border-red-100">
            Error: {submitError}
          </p>
        )}

        {/* Action Buttons */}
        <div className="flex justify-between items-center mt-8 pt-4 border-t border-gray-100">
          <Button
            type="button"
            variant="outline"
            onClick={handleBack}
            disabled={stepIndex === 0 || isSubmitting}
            className="px-6 py-2.5 h-11 border border-gray-300 text-[#1A2B4C] font-medium rounded-lg hover:bg-gray-100 hover:text-black transition-all cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Back
          </Button>

          <Button
            type="button"
            onClick={handleNext}
            disabled={isSubmitting}
            className="px-6 py-2.5 h-11 bg-[#1A2B4C] hover:bg-[#1F8C8C] text-white font-medium rounded-lg shadow-md hover:shadow-lg transition-all cursor-pointer active:scale-95 disabled:opacity-50"
          >
            {isSubmitting ? "Creating..." : isLastStep ? "Create Video" : "Next"}
          </Button>
        </div>

      </div>
    </div>
  );
}
/**
 * Project Types
 */

export interface Project {
    id: string;
    name: string;
    description?: string | null;
    status: "planning" | "active" | "on_hold" | "completed" | "archived";
    start_date?: string | null;
    end_date?: string | null;
    budget?: number | null;
    created_at: string;
    updated_at: string;
}

export interface ProjectFormData {
    name: string;
    description?: string;
    status: "planning" | "active" | "on_hold" | "completed" | "archived";
    start_date?: string;
    end_date?: string;
    budget?: number;
}

/**
 * Task Types
 */

export interface Task {
    id: string;
    title: string;
    description?: string | null;
    status: "todo" | "in_progress" | "review" | "done";
    priority: "low" | "medium" | "high" | "urgent";
    project_id?: string | null;
    assigned_to_id?: string | null;
    due_date?: string | null;
    created_at: string;
    updated_at: string;
}

export interface TaskFormData {
    title: string;
    description?: string;
    status: "todo" | "in_progress" | "review" | "done";
    priority: "low" | "medium" | "high" | "urgent";
    project_id?: string;
    assigned_to_id?: string;
    due_date?: string;
}

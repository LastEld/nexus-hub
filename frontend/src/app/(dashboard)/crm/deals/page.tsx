"use client";

import { useState } from "react";
import { Plus, Search, Filter, TrendingUp, DollarSign } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface Deal {
    id: string;
    name: string;
    company: string;
    value: number;
    stage: string;
    probability: number;
    expectedCloseDate: string;
    tags?: string[];
}

const stages = [
    { id: "lead", name: "Lead", color: "bg-gray-500" },
    { id: "qualified", name: "Qualified", color: "bg-blue-500" },
    { id: "proposal", name: "Proposal", color: "bg-purple-500" },
    { id: "negotiation", name: "Negotiation", color: "bg-orange-500" },
    { id: "closed_won", name: "Closed Won", color: "bg-green-500" },
];

export default function DealsPage() {
    const [searchTerm, setSearchTerm] = useState("");
    const [deals] = useState<Deal[]>([
        {
            id: "1",
            name: "Enterprise Platform Deal",
            company: "Acme Corporation",
            value: 250000,
            stage: "proposal",
            probability: 70,
            expectedCloseDate: "2024-12-31",
            tags: ["enterprise", "saas"],
        },
        {
            id: "2",
            name: "Manufacturing System",
            company: "Globex Industries",
            value: 150000,
            stage: "qualified",
            probability: 50,
            expectedCloseDate: "2025-01-15",
            tags: ["manufacturing"],
        },
        {
            id: "3",
            name: "Consulting Services",
            company: "Initech",
            value: 75000,
            stage: "negotiation",
            probability: 85,
            expectedCloseDate: "2024-12-20",
            tags: ["consulting"],
        },
    ]);

    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat("en-US", {
            style: "currency",
            currency: "USD",
            minimumFractionDigits: 0,
        }).format(value);
    };

    const totalValue = deals.reduce((sum, deal) => sum + deal.value, 0);
    const weightedValue = deals.reduce(
        (sum, deal) => sum + (deal.value * deal.probability) / 100,
        0
    );

    const dealsByStage = stages.map((stage) => ({
        ...stage,
        deals: deals.filter((d) => d.stage === stage.id),
    }));

    return (
        <div className="flex flex-col gap-6 p-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Deal Pipeline</h1>
                    <p className="text-muted-foreground">
                        Manage your sales opportunities and track progress
                    </p>
                </div>
                <Button size="sm">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Deal
                </Button>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Total Pipeline
                        </CardTitle>
                        <DollarSign className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{formatCurrency(totalValue)}</div>
                        <p className="text-xs text-muted-foreground">
                            {deals.length} active deals
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Weighted Pipeline
                        </CardTitle>
                        <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {formatCurrency(weightedValue)}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Based on probability
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">67%</div>
                        <p className="text-xs text-muted-foreground">
                            Last 30 days
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Avg Deal Size</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {formatCurrency(totalValue / deals.length)}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Current pipeline
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Search */}
            <div className="flex items-center gap-2">
                <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        placeholder="Search deals..."
                        className="pl-8"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <Button variant="outline" size="sm">
                    <Filter className="h-4 w-4 mr-2" />
                    Filters
                </Button>
            </div>

            {/* Kanban Board */}
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
                {dealsByStage.map((stage) => (
                    <Card key={stage.id} className="flex flex-col">
                        <CardHeader className="pb-3">
                            <div className="flex items-center justify-between">
                                <CardTitle className="text-sm font-medium">
                                    {stage.name}
                                </CardTitle>
                                <Badge variant="secondary" className="h-6">
                                    {stage.deals.length}
                                </Badge>
                            </div>
                            <CardDescription className="text-xs">
                                {formatCurrency(
                                    stage.deals.reduce((sum, d) => sum + d.value, 0)
                                )}
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 space-y-2">
                            {stage.deals.map((deal) => (
                                <Card
                                    key={deal.id}
                                    className="p-3 cursor-pointer hover:shadow-md transition-shadow border-l-4"
                                    style={{ borderLeftColor: stage.color.replace("bg-", "") }}
                                >
                                    <div className="space-y-2">
                                        <div className="font-medium text-sm line-clamp-2">
                                            {deal.name}
                                        </div>
                                        <div className="text-xs text-muted-foreground">
                                            {deal.company}
                                        </div>
                                        <div className="flex items-center justify-between text-xs">
                                            <span className="font-semibold">
                                                {formatCurrency(deal.value)}
                                            </span>
                                            <span className="text-muted-foreground">
                                                {deal.probability}%
                                            </span>
                                        </div>
                                        <Progress value={deal.probability} className="h-1" />
                                        <div className="flex gap-1">
                                            {deal.tags?.map((tag) => (
                                                <Badge
                                                    key={tag}
                                                    variant="outline"
                                                    className="text-xs px-1.5 py-0"
                                                >
                                                    {tag}
                                                </Badge>
                                            ))}
                                        </div>
                                    </div>
                                </Card>
                            ))}
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}

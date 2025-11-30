"use client";

import { useState } from "react";
import { Plus, Search, Filter, Download, Upload, MoreVertical, Pencil, Trash2 } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";
import { useCompanies, useDeleteCompany } from "@/features/crm/hooks/use-companies";
import { Company } from "@/types/crm";
import { CompanyForm } from "@/features/crm/components/company-form";

export default function CompaniesPage() {
    const [searchTerm, setSearchTerm] = useState("");
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [selectedCompany, setSelectedCompany] = useState<Company | undefined>();
    const { data: companies, isLoading, error } = useCompanies();
    const deleteCompany = useDeleteCompany();

    const handleDelete = async (id: string) => {
        if (confirm("Are you sure you want to delete this company?")) {
            await deleteCompany.mutateAsync(id);
        }
    };

    const handleEdit = (company: Company) => {
        setSelectedCompany(company);
        setIsFormOpen(true);
    };

    const handleCreate = () => {
        setSelectedCompany(undefined);
        setIsFormOpen(true);
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case "customer":
                return "bg-green-100 text-green-800";
            case "prospect":
                return "bg-blue-100 text-blue-800";
            case "lead":
                return "bg-yellow-100 text-yellow-800";
            case "inactive":
                return "bg-gray-100 text-gray-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    const filteredCompanies = companies?.filter((company: Company) =>
        company.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="flex flex-col gap-6 p-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Companies</h1>
                    <p className="text-muted-foreground">
                        Manage your company relationships and accounts
                    </p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                        <Upload className="h-4 w-4 mr-2" />
                        Import
                    </Button>
                    <Button variant="outline" size="sm">
                        <Download className="h-4 w-4 mr-2" />
                        Export
                    </Button>
                    <Button size="sm" onClick={handleCreate}>
                        <Plus className="h-4 w-4 mr-2" />
                        Add Company
                    </Button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Total Companies
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{companies?.length || 0}</div>
                        <p className="text-xs text-muted-foreground">
                            All companies in CRM
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Active Customers
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {companies?.filter((c: Company) => c.status === "customer").length || 0}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Paying customers
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Prospects</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {companies?.filter((c: Company) => c.status === "prospect").length || 0}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Potential customers
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Industries</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {new Set(companies?.map((c: Company) => c.industry).filter(Boolean)).size || 0}
                        </div>
                        <p className="text-xs text-muted-foreground">Unique sectors</p>
                    </CardContent>
                </Card>
            </div>

            {/* Search and Filters */}
            <div className="flex items-center gap-2">
                <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        placeholder="Search companies..."
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

            {/* Companies Table */}
            <Card>
                <CardHeader>
                    <CardTitle>All Companies</CardTitle>
                    <CardDescription>
                        A list of all companies in your CRM
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <div className="flex items-center justify-center h-64">
                            <div className="text-center">
                                <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary mx-auto"></div>
                                <p className="mt-4 text-sm text-muted-foreground">Loading companies...</p>
                            </div>
                        </div>
                    ) : error ? (
                        <div className="flex items-center justify-center h-64">
                            <div className="text-center">
                                <p className="text-destructive">Error loading companies</p>
                                <p className="text-sm text-muted-foreground mt-2">{error.message}</p>
                            </div>
                        </div>
                    ) : filteredCompanies && filteredCompanies.length > 0 ? (
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Industry</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Location</TableHead>
                                    <TableHead>Contact</TableHead>
                                    <TableHead>Tags</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredCompanies.map((company: Company) => (
                                    <TableRow key={company.id} className="hover:bg-muted/50">
                                        <TableCell className="font-medium">
                                            <Link
                                                href={`/crm/companies/${company.id}`}
                                                className="text-primary hover:underline"
                                            >
                                                {company.name}
                                            </Link>
                                        </TableCell>
                                        <TableCell>{company.industry || "-"}</TableCell>
                                        <TableCell>
                                            <Badge className={getStatusColor(company.status)} variant="outline">
                                                {company.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            {company.city && company.country
                                                ? `${company.city}, ${company.country}`
                                                : company.country || "-"}
                                        </TableCell>
                                        <TableCell className="text-sm text-muted-foreground">
                                            {company.email || company.phone || "-"}
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-1">
                                                {company.tags?.slice(0, 2).map((tag) => (
                                                    <Badge key={tag} variant="secondary" className="text-xs">
                                                        {tag}
                                                    </Badge>
                                                ))}
                                                {(company.tags?.length || 0) > 2 && (
                                                    <Badge variant="secondary" className="text-xs">
                                                        +{(company.tags?.length || 0) - 2}
                                                    </Badge>
                                                )}
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <DropdownMenu>
                                                <DropdownMenuTrigger asChild>
                                                    <Button variant="ghost" size="icon">
                                                        <MoreVertical className="h-4 w-4" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem onClick={() => handleEdit(company)}>
                                                        <Pencil className="mr-2 h-4 w-4" />
                                                        Edit
                                                    </DropdownMenuItem>
                                                    <DropdownMenuItem
                                                        className="text-destructive"
                                                        onClick={() => handleDelete(company.id)}
                                                    >
                                                        <Trash2 className="mr-2 h-4 w-4" />
                                                        Delete
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    ) : (
                        <div className="flex items-center justify-center h-64">
                            <div className="text-center">
                                <p className="text-muted-foreground">No companies found</p>
                                <Button className="mt-4" onClick={handleCreate}>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Add Your First Company
                                </Button>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Company Form Dialog */}
            <CompanyForm
                open={isFormOpen}
                onOpenChange={(open) => {
                    setIsFormOpen(open);
                    if (!open) setSelectedCompany(undefined);
                }}
                company={selectedCompany}
            />
        </div>
    );
}

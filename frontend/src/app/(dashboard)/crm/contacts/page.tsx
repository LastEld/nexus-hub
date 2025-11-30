"use client";

import { useState } from "react";
import { Plus, Search, Filter, Download, Upload, Mail, Phone } from "lucide-react";
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
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

interface Contact {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
    company?: string;
    title?: string;
    leadStatus?: string;
    rating?: number;
    tags?: string[];
}

export default function ContactsPage() {
    const [searchTerm, setSearchTerm] = useState("");
    const [contacts] = useState<Contact[]>([
        {
            id: "1",
            firstName: "John",
            lastName: "Doe",
            email: "john.doe@acme.com",
            phone: "+1-555-0101",
            company: "Acme Corporation",
            title: "CEO",
            leadStatus: "qualified",
            rating: 5,
            tags: ["decision-maker", "tech"],
        },
        {
            id: "2",
            firstName: "Jane",
            lastName: "Smith",
            email: "jane.smith@globex.com",
            phone: "+1-555-0202",
            company: "Globex Industries",
            title: "VP Sales",
            leadStatus: "contacted",
            rating: 4,
            tags: ["sales"],
        },
    ]);

    const getStatusColor = (status?: string) => {
        switch (status) {
            case "qualified":
                return "bg-green-100 text-green-800";
            case "contacted":
                return "bg-blue-100 text-blue-800";
            case "new":
                return "bg-yellow-100 text-yellow-800";
            case "lost":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    const getInitials = (firstName: string, lastName: string) => {
        return `${firstName[0]}${lastName[0]}`.toUpperCase();
    };

    const filteredContacts = contacts.filter(
        (contact) =>
            contact.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            contact.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            contact.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="flex flex-col gap-6 p-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Contacts</h1>
                    <p className="text-muted-foreground">
                        Manage your professional contacts and leads
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
                    <Button size="sm">
                        <Plus className="h-4 w-4 mr-2" />
                        Add Contact
                    </Button>
                </div>
            </div>

            {/* Stats Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Total Contacts
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{contacts.length}</div>
                        <p className="text-xs text-muted-foreground">
                            Active in CRM
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            Qualified Leads
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {contacts.filter((c) => c.leadStatus === "qualified").length}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Ready for sales
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">New Contacts</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {contacts.filter((c) => c.leadStatus === "new").length}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            This month
                        </p>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">High Priority</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {contacts.filter((c) => (c.rating || 0) >= 4).length}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Rating 4+
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Search and Filters */}
            <div className="flex items-center gap-2">
                <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                        placeholder="Search contacts..."
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

            {/* Contacts Table */}
            <Card>
                <CardHeader>
                    <CardTitle>All Contacts</CardTitle>
                    <CardDescription>
                        A list of all contacts in your CRM
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Company</TableHead>
                                <TableHead>Title</TableHead>
                                <TableHead>Contact Info</TableHead>
                                <TableHead>Lead Status</TableHead>
                                <TableHead>Rating</TableHead>
                                <TableHead>Tags</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredContacts.map((contact) => (
                                <TableRow key={contact.id} className="cursor-pointer hover:bg-muted/50">
                                    <TableCell>
                                        <div className="flex items-center gap-3">
                                            <Avatar className="h-9 w-9">
                                                <AvatarFallback className="text-xs">
                                                    {getInitials(contact.firstName, contact.lastName)}
                                                </AvatarFallback>
                                            </Avatar>
                                            <div>
                                                <div className="font-medium">
                                                    {contact.firstName} {contact.lastName}
                                                </div>
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>{contact.company || "-"}</TableCell>
                                    <TableCell className="text-muted-foreground">
                                        {contact.title || "-"}
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex flex-col gap-1 text-sm">
                                            <div className="flex items-center gap-1">
                                                <Mail className="h-3 w-3 text-muted-foreground" />
                                                <span className="text-xs">{contact.email}</span>
                                            </div>
                                            {contact.phone && (
                                                <div className="flex items-center gap-1">
                                                    <Phone className="h-3 w-3 text-muted-foreground" />
                                                    <span className="text-xs">{contact.phone}</span>
                                                </div>
                                            )}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge
                                            className={getStatusColor(contact.leadStatus)}
                                            variant="outline"
                                        >
                                            {contact.leadStatus || "unknown"}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex gap-0.5">
                                            {Array.from({ length: contact.rating || 0 }).map((_, i) => (
                                                <span key={i} className="text-yellow-500">★</span>
                                            ))}
                                            {Array.from({ length: 5 - (contact.rating || 0) }).map((_, i) => (
                                                <span key={i} className="text-gray-300">★</span>
                                            ))}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex gap-1">
                                            {contact.tags?.slice(0, 2).map((tag) => (
                                                <Badge key={tag} variant="secondary" className="text-xs">
                                                    {tag}
                                                </Badge>
                                            ))}
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
